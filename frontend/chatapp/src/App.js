import logo from './logo.svg';
import './App.css';
import Admin from './Admin';
import { BrowserRouter, Routes, Route, Router, Switch} from "react-router-dom";
import Button from '@mui/material/Button';
import ReactDOM from 'react';
import Login from './Login';
import Home from './Home';
import Register from './Register'
import { useNavigate,navigate } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <Login />} />
        <Route path="/admin" element ={<PrivateRoute component={Admin} />} />
        <Route path="/login" element = {<Login />} />
        <Route path="/register" element = {<Register/>} />
        <Route path="/home" element = {<PrivateRoute component={Home}/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

