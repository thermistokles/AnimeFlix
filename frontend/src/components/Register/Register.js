import React, { FC, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Button, Dropdown } from 'react-bootstrap';
import './Register.css'

export default function (props) {

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [user, setUser] = useState();

  const options = [
    "Actions",
    "Comedy",
    "Romance",
    "Sci-Fi",
    "Adventure",
  ];

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    genres: [],
    isOver18: false,
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
    const isOver18 = event.target.checked;
    setFormData({ ...formData, isOver18 });
  };

  const handleMovieShowChange = (event) => {
    setFormData({ ...formData, movieShow: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData);

    
  };



   return (
      <div className="Auth-form-container">
        <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input type="text" value={formData.username} onChange={handleUsernameChange} />
      </label>
      <label>
        Password:
        <input type="password" value={formData.password} onChange={handlePasswordChange} />
      </label>
      <label>
        Favorite Genres:
        <select multiple={true} value={formData.genres} onChange={handleGenresChange}>
          <option value="">--Select Genre--</option>
          <option value="Action">Action</option>
          <option value="Comedy">Comedy</option>
          <option value="Drama">Drama</option>
          <option value="Horror">Horror</option>
        </select>
      </label>
      <label>
        Are you over 18?
        <input type="checkbox" checked={formData.isOver18} onChange={handleAgeChange} />
      </label>
      <label>
        Movie/Show:
        <select value={formData.movieShow} onChange={handleMovieShowChange}>
          <option value="Movie">Movie</option>
          <option value="Show">Show</option>
        </select>
      </label>
      <button type="submit">Register</button>
    </form>
      </div>
    )
}
