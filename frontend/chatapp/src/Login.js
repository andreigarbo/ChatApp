import React, { useState } from 'react';
import { TextField, Button, Card, CardContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);


    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleLogin = () => {
        axios.post('http://127.0.0.1:8000/login', {username, password})
            .then(response => {
                sessionStorage.setItem('token', response.data.token);
                sessionStorage.setItem('is_admin', response.data.is_admin);
                console.log("TOKEN " + response.data.token);
                console.log("IS ADMIN " + response.data.is_admin);
                if(response.data.is_admin == true)
                    navigate('/admin');
                else
                    navigate('/home');
            })
            .catch(error => {
                console.error(error);
                setError(error.response.data.reason);
                setTimeout(() => {
                    setError('');
                }, 5000);
            });

    };


    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#32ADCD' }}>
            <Card style={{ minWidth: '700px', minHeight: '400px' }}>
                <CardContent>
                    <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Login to your Account</h2>
                    <TextField label="Username" variant="outlined" value={username} onChange={handleUsernameChange} style={{ marginBottom: '1rem', width: '100%' }} />
                    <TextField label="Password" variant="outlined" type="password" value={password} onChange={handlePasswordChange} style={{ marginBottom: '1rem', width: '100%' }} />
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                        <Button variant="contained" style={{backgroundColor: '#CD5232', color: '#FFFFFF', marginRight: '1rem' }} onClick={handleLogin}>
                            Login
                        </Button>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '1rem' }}>
                        <span style={{ marginBottom: '0.5rem' }}>Don't have an account?</span>
                        <Button variant="text" style={{backgroundColor: '#CD5232', color: '#FFFFFF', marginRight: '1rem' }} onClick={() => navigate('/register')}>
                            Create account
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default Login;
