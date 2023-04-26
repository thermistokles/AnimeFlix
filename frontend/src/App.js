import logo from './logo.svg';
import React, { FC, useState } from 'react';
import './App.css';
import { Route, Switch, BrowserRouter, Redirect } from "react-router-dom";
import { useHistory } from 'react-router-dom';
import Register from './components/Register/Register';
import Login from './components/Login/Login';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
  const history = useHistory();

  return (
      // <Switch>
      //   <Route path="/dashboard" component={Dashboard}><Dashboard data={userData} /></Route>
      //   <Route path="/login"><Login onSendData={handleUserData}/></Route>
      //   <Route path="/register" component={Register} />
      // </Switch>

    
      <Switch>
        <Route exact path="/"><Login /></Route>
        <Route path="/dashboard" ><Dashboard /></Route>
        <Route path="/login"><Login /></Route>
        <Route path="/register"><Register /></Route>
      </Switch>
  );
}

export default App;
