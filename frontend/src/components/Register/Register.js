import React, { FC, useState } from 'react';
import { useHistory } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Button, Dropdown } from 'react-bootstrap';
import './Register.css';
import Login from '../Login/Login'
import axios from 'axios';
import { BrowserRouter, Routes, Router, Route, Switch, Redirect } from "react-router-dom";
import Dashboard from '../Dashboard/Dashboard';

export default function (props) {

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [user, setUser] = useState();
  const history = useHistory();

  const options = [
    "Actions",
    "Comedy",
    "Romance",
    "Sci-Fi",
    "Adventure",
    "Shounen",
    "Drama",
    "Sports",

  ];

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    genres: [],
    isOver18: 0,
    movieShow: ''
  });

  const handleUsernameChange = (event) => {
    setFormData({ ...formData, username: event.target.value });
  };

  const handlePasswordChange = (event) => {
    setFormData({ ...formData, password: event.target.value });
  };

  const handleGenresChange = (event) => {
    const selectedGenres = Array.from(event.target.selectedOptions, (option) => option.value);
    setFormData({ ...formData, genres: selectedGenres });
  };

  const handleAgeChange = (event) => {
    setFormData({ ...formData, isOver18: parseInt(event.target.value) });
  };

  const handleMovieShowChange = (event) => {
    setFormData({ ...formData, movieShow: event.target.value });
  };

  localStorage.clear()

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData);

    axios.post('http://127.0.0.1:5000/register', formData)
  .then(response => {

    if(response.data == "registered successfully"){
      console.log(response.data);
    var username = formData.username;
    var authMethod = "register"
    localStorage.setItem('username', JSON.stringify(username));
    localStorage.setItem('isOver18', JSON.stringify(formData.isOver18));
    localStorage.setItem('genres', JSON.stringify(formData.genres));
    localStorage.setItem('movieShow', JSON.stringify(formData.movieShow));
    localStorage.setItem('authMethod', JSON.stringify(authMethod));
    history.push('/dashboard');
    }
    else{
      console.log(response.data)
    }
    
  })
  .catch(error => {
    console.error(error);
  });
  };

  const handleLoginClick = () => {
    history.push('/login');
  }


   return (
      <div className="Auth-form-container">
      <h1 className='header'>Registration</h1>
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
        <label>
          Favorite Genres:
          <select
            multiple={true}
            value={formData.genres}
            onChange={handleGenresChange}
          >
            <option value="">--Select Genre--</option>
            <option value="Action">Action</option>
            <option value="Comedy">Comedy</option>
            <option value="Drama">Drama</option>
            <option value="Horror">Horror</option>
          </select>
        </label>
        <label>
          Enter your age
          <input
            type="number"
            value={formData.isOver18}
            onChange={handleAgeChange}
          />
        </label>
        <label>
          Movie/Show:
          <select
            value={formData.movieShow}
            onChange={handleMovieShowChange}
          >
            <option value="Movie">Movie</option>
            <option value="Show">Show</option>
          </select>
        </label>
        <button type="submit">Register</button>
      </form>
      <p className='registerText'>Already have an account?</p>
      <button type="button" onClick={handleLoginClick}>
        Login
      </button>
    </div>

      
    )
}
