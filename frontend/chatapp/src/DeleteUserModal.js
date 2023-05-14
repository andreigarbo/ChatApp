import React from 'react';
import { useState } from 'react';
import Modal from '@mui/material/Modal'
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { List, ListItem, ListItemText } from '@mui/material';

function DeleteUserModal(props){
    const { open, onClose, users, handleUserDelete } = props;

    const [selectedUser, setSelectedUser] = useState(null);

    const handleUserSelect = (user) => {
        setSelectedUser(user);
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
            }}>
            {users.map((user) => (
            <ListItem
              key={user}
              button
              selected={selectedUser && selectedUser === user}
              onClick={() => handleUserSelect(user)}
              sx={{
                backgroundColor: selectedUser && selectedUser === user ? '#f2f2f2' : 'inherit',
            }}
            >
              <ListItemText primary={user} />
            </ListItem>
            ))}
          {selectedUser && <div style={{ marginBottom: '1rem', marginTop: '1rem', width: '100%' }}>Selected user: {selectedUser}</div>}
          <Button variant="contained" color="primary" onClick={() => handleUserDelete(selectedUser)}> Delete User </Button>
          </Box>
        </Modal>
    );
}

export default DeleteUserModal;