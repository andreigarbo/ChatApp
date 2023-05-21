import { useEffect, useState } from 'react';
import { List, ListItem, ListItemAvatar, ListItemText, Avatar, TextField, Button, ListItemButton } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import io from 'socket.io-client'; 

const socket = io('http://localhost:8000');

function Home() {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState('nul');
  const [messageBar, setMessageBar] = useState('');
  const [pollingStarted, setPollingStarted] = useState(false);
  const currentUser = sessionStorage.getItem('logged-in-as');
  console.log("CURRENT USER " + currentUser);
  const navigate = useNavigate();

  const handleSelectUser = (user) =>{
    setSelectedUser(user);
  }

  useEffect(() => {
    socket.on('data_response', (data) => {
      if((data.from == currentUser || data.from == selectedUser) && (data.to == currentUser || data.to == selectedUser)){
        console.log("data from " + data.from);
        console.log("data to " + data.to);
        console.log("current user " + currentUser);
        console.log("selected user " + selectedUser);
        fetchMessageTest();
      }
    });

    return () => {
      socket.off('data_response');
    };
  }, []);

  useEffect(() =>  {
    if(selectedUser != 'nul'){
      //setPollingStarted(true);
      fetchMessageTest();
    }
  }, [selectedUser]);

  const pollMessages = async () => {
    try {
      fetchMessageTest();
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };
  
  const startPolling = () => {
    if(pollingStarted){
      pollMessages(); 
      setInterval(pollMessages, 5000);
    }
  };

  useEffect(() => {
    startPolling();
    return () =>{
    };
  }, [pollingStarted]);
  
  const handleMessageBarChange = (event) => {
    setMessageBar(event.target.value);
  }

  const handleSetUsers = () => {
    axios.get(`http://127.0.0.1:8000/get-user-list`)
    .then(response => {
        setUsers(response.data.users);
    })
    .catch(error =>{
        console.log(error);
    })
  }

  useEffect(() => {
      handleSetUsers();
  }, []);


  const handleSend = () => {
    axios.request({
      method: 'POST',
      url: 'http://127.0.0.1:8000/send-message',
      headers: {
          sender: currentUser,
          receiver: selectedUser,
          content: messageBar
      }
    })
    .then(response => {
        fetchMessageTest();
        //setNewMessage('');
      })
      .catch(error => {
        console.error(error);
      });
    };


    const handleLogOut = () => {
      console.log(sessionStorage.getItem('token'));
      axios.request({
          method: 'POST',
          url: 'http://127.0.0.1:8000/logout',
          headers: {
              Authorization: `${sessionStorage.getItem('token')}`
          }
      })
      .then(response => {
          sessionStorage.setItem('token', 'nul');
          navigate('/login');
          console.log("TOKEN SHOULD BE NULL: " + sessionStorage.getItem('token'));
      })
      .catch(error => {
          console.log(error);
      });
    }

    const fetchMessageTest = () => {
      console.log("SEDNING REQUEST WITH " + currentUser + " " + selectedUser);
      axios.request({
        method: 'GET',
        url: 'http://127.0.0.1:8000/messages-between',
        headers: {
            userone: currentUser,
            usertwo: selectedUser
        }
    })
      .then(response => {
        setMessages([]);
        setMessages(response.data.messages);
        console.log("RESPONSE DATA MSG")
        console.log()
      })
      .catch(error => {
        console.log(error);
      })
    }

    useEffect(() =>{
      console.log("MESSAGES CHANGED");
      console.log(messages);
    }, [messages])

  return (
  <div style={{ display: 'flex', height: '100vh'}}>
    <div style={{ flex: '1 1 auto', maxWidth: '10%', minWidth: '5%', background: '#32ADCD', marginRight: '1rem'}}>
      <List>
        {users.map((user) => (
          <ListItem disablePadding key={user.id} selected={user === selectedUser}>
            <ListItemButton onClick={() => handleSelectUser(user)}>
              <ListItemText primary={user} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Button variant="contained" onClick={handleLogOut} style={{ position: 'absolute', bottom: 0, marginBottom: '1rem', marginLeft: '1.5rem' }}>Log Out</Button>
    </div>
    <div style={{ flex: '1 1 auto', height: '100vh', display: 'flex', flexDirection: 'column' }}>
    <h1>Chat App</h1>
    <div style={{ display: 'flex', alignItems: 'center', padding: '1rem' }}>
        <h3>Chatting to: </h3>
        <h2 style={{ margin: '0 1rem' }}>{selectedUser}</h2>
    </div>
    <div style={{ flex: '1 1 auto', overflowY: 'auto' }}>
      <div style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>
        <List key={messages}>
        {messages.length > 1 ? (
          messages.map((message) => (
          <ListItem key={message[0]}>
            <ListItemAvatar>
            <Avatar>{message[0][0]}</Avatar>
            </ListItemAvatar>
            <ListItemText primary={message[0] === currentUser ? "You" : message[0]} secondary={message[1]} />
          </ListItem>
        ))
        ) : (
          <ListItem>
            <ListItemText primary="No messages" />
          </ListItem>
        )}
        </List>
      </div>
    </div>
    <TextField label="New Message" variant="outlined" value={messageBar} onChange={handleMessageBarChange}></TextField>
    <Button variant="contained" onClick={handleSend} style={{marginBottom:'1rem'}}>Send</Button>
  </div>
</div>
  );
}

export default Home;
