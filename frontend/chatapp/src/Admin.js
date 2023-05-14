
import React, { useState,useEffect  } from 'react';
import Button from '@mui/material/Button';
import EditUserModal from './EditUserModal';
import DeleteUserModal from './DeleteUserModal';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';



function Admin(){
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [users, setUsers] = useState([]);

    const navigate = useNavigate();

    const handleEditModalOpen = () => {
        setEditModalOpen(true);
    };

    const handleEditModalClose = () => {
        setEditModalOpen(false);
    };

    const handleDeleteModalOpen = () => {
        setDeleteModalOpen(true);
    };

    const handleDeleteModalClose = () => {
        setDeleteModalOpen(false);
    };

    const handleSetUsers = () => {
        axios.get(`http://127.0.0.1:8000/get-user-list`)
        .then(response => {
            setUsers(response.data.users);
            console.log(response.data);
            console.log(response.data.users);
        })
        .catch(error =>{
            console.log(error);
        })
    }
    
    const handleUserDelete = (user) => {
        console.log("DELETING" + user);
        axios.post(`http://127.0.0.1:8000/delete-user`, {user})
        .then(response => {
          console.log('User deleted successfully');
        })
        .catch(error => {
          console.error('Error reaching the server:', error);
        })
        .then(handleSetUsers);
        
    }

    const handleUserEdit = (selectedUser, password) => {
        console.log(selectedUser + password);
        axios.post(`http://127.0.0.1:8000/admin-change-password`, {selectedUser, password})
        .then(response => {
            console.log("Changed password status: " + response.data.status)
        })
        .catch(error => {
            console.error('Error reaching the server:', error);
        })
    
    }

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

    useEffect(() => {
        handleSetUsers();
    }, []);


    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Button variant="contained" color="primary" onClick={handleEditModalOpen}>
                    Edit User
                </Button>
                <Button variant="contained" color="secondary" onClick={handleDeleteModalOpen}>
                    Delete User
                </Button>
                <Button variant="contained" color="primary" onClick={handleLogOut}>
                    Log out
                </Button>
                <EditUserModal open={editModalOpen} onClose={handleEditModalClose} users={users} handleUserEdit={handleUserEdit}/>
                <DeleteUserModal open={deleteModalOpen} onClose={handleDeleteModalClose} users={users} handleUserDelete={handleUserDelete}/>
            </div>
        </div>
      );
}

export default Admin;
