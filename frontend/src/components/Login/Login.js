import React, { FC, useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import { BrowserRouter, Routes, Router, Route, Switch, Redirect } from "react-router-dom";
import Dashboard from '../Dashboard/Dashboard';

function Login (props) {

    const [user, setUser] = useState();
    const history = useHistory();
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

        axios.post('http://127.0.0.1:5000/login', formData)
        .then(response => {
          console.log("response.data: ", response.data)
            props.onSendData(response.data)
            
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

export default Login;