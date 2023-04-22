import React, { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function (props) {

    const [user, setUser] = useState();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: ''
      });

    const handleUsernameChange = (event) => {
    setFormData({ ...formData, username: event.target.value });
    };

    const handlePasswordChange = (event) => {
    setFormData({ ...formData, password: event.target.value });
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(formData);

        axios.post('http://127.0.0.1:5000/login', formData)
        .then(response => {
            if(response.data == 'Logged in'){
                console.log("logged in")
                navigate('/dashboard');
            }
            else{
                console.log("not logged in")
            }
        })
        .catch(error => {
            console.error(error);
        });
      };

    return(
        <div className="Auth-form-container">
            <h1>Login</h1>
        <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input type="text" value={formData.username} onChange={handleUsernameChange} />
      </label>
      <label>
        Password:
        <input type="password" value={formData.password} onChange={handlePasswordChange} />
      </label>
      <button type="submit">Login</button>
    </form>
      </div>
    )
}