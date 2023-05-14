import React, { useState } from 'react';
import { TextField, Button,Card, CardContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Register() {

    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleRegister = () => {
        axios.post('http://127.0.0.1:8000/create-user', {username, password, email})
            .then(response => {
                navigate('/login');
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
            <Card style={{ minWidth: '700px',minHeight:'400px' }}>
            <CardContent>
        
                <h2 style={{ textAlign: 'center', color: '#000000' }}>Create a new Account</h2>
                <TextField label="Email" variant="outlined" value={email} onChange={handleEmailChange} style={{ marginBottom: '1rem', width: '100%' }} />
                <TextField label="Username" variant="outlined" value={username} onChange={handleUsernameChange} style={{ marginBottom: '1rem', width: '100%' }} />
                <TextField label="Password" variant="outlined" type="password" value={password} onChange={handlePasswordChange} style={{ marginBottom: '1rem', width: '100%' }} />
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                    <Button variant="contained" style={{ backgroundColor: '#CD5232', color: '#FFFFFF', marginRight: '1rem' }} onClick={handleRegister}>
                        Register
                    </Button>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '1rem' }}>
                    <span style={{ marginBottom: '0.5rem' }}>Already have an account?</span>
                    <Button variant="text" style={{backgroundColor: '#CD5232', color: '#FFFFFF', marginRight: '1rem' }} onClick={() => navigate('/login')}>
                        Login
                    </Button>
                </div>
            
            </CardContent>
            </Card>
        </div>
    );
}

export default Register;
