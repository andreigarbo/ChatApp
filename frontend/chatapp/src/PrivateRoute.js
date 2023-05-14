import { useEffect,useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import Admin from './Admin';


function PrivateRoute({ component: Component, ...rest }) {
    const navigate = useNavigate();
    const [token, setToken] = useState(sessionStorage.getItem('token'));

    useEffect(() => {
        setToken(sessionStorage.getItem('token'));
    }, []);

    console.log("LOGGIN FROM PROTECTOR " + token);

    if (token === 'nul' || !token) {
        console.log("TOKEN IS NULL")
        return <Navigate to="/login" replace />;
    }
    else{
        if (Component === Admin) {
            const isAdmin = sessionStorage.getItem('is_admin');
            if (isAdmin === 'true') {
              return <Component {...rest} />;
            } else {
              return <Navigate to="/home" replace />;
            }
          } else {
            return <Component {...rest} />;
        }
    }
}

export default PrivateRoute;
