import React from 'react';
import { useState } from 'react';
import Modal from '@mui/material/Modal'
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { List, ListItem, ListItemText } from '@mui/material';
import TextField from '@mui/material/TextField';

function EditUserModal(props){
    const { open, onClose, users, handleUserEdit } = props;
    const [selectedUser, setSelectedUser] = useState(null);
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUserSelect = (user) => {
        setSelectedUser(user);
        console.log("selected user " + user);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleEditButtonClick = () => {
        handleUserEdit(selectedUser,password);
    };


    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 400,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    p: 4,
                    display: 'flex',
                    flexDirection: 'column',
                    //alignItems: 'center',
                }}>
                <List sx={{ mb: 2 }}>
                    {users.map((user) => (
                        <ListItem
                        key={user}
                        button
                        selected={selectedUser && selectedUser === user}
                        onClick={() => handleUserSelect(user)}
                        sx={{
                            backgroundColor: selectedUser && selectedUser.id === user.id ? '#f2f2f2' : 'inherit',
                        }}
                        >
                        <ListItemText primary={user} />
                        </ListItem>
                    ))}
                </List>
                {selectedUser && <div style={{ marginBottom: '1rem', width: '100%' }}>Selected user: {selectedUser}</div>}
                <TextField id="outlined-basic" label="Password" style={{marginBottom: '1rem'}} variant="outlined" onChange={handlePasswordChange}></TextField>
                <Button variant="contained" color="primary" onClick={handleEditButtonClick}> Edit User </Button>
            </Box>
        </Modal>
    );
}

export default EditUserModal;