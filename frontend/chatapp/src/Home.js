import React, { useState } from 'react';
import { TextField, Button, Card, CardContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


  function Home() {

    const navigate = useNavigate();

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

    return (
      <div>
        <h1>Hello, World!</h1>
        <Button variant="contained" color="primary" onClick={handleLogOut}>
            Log Out
        </Button>
      </div>
    );
  }

export default Home;
