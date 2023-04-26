import React, { FC, useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import { BrowserRouter, Routes, Router, Route, Switch, Redirect } from "react-router-dom";
import Dashboard from '../Dashboard/Dashboard';
import "./Login.css";

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

          if(response.data == "Logged In"){
            var username = formData.username;
            var authMethod = "login"
            localStorage.setItem('username', JSON.stringify(username));
            localStorage.setItem('authMethod', JSON.stringify(authMethod));
            history.push('/dashboard')   
          }   
          else{
            console.log(response.data)
          }   
        })
        .catch(error => {
            console.error(error);
        });
      };

      const handleRegisterClick = () => {
        history.push('/register');
      }

    return(
      <div className="Auth-form-container">
      <h1 className='header'>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            value={formData.username}
            onChange={handleUsernameChange}
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={formData.password}
            onChange={handlePasswordChange}
          />
        </label>
        <button type="submit">Login</button>
      </form>
      <p className='loginText'>Don't have an account?</p>
      <button type="button" onClick={handleRegisterClick}>
        Register
      </button>
    </div>
    )
}

export default Login;