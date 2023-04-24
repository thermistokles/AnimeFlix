import logo from './logo.svg';
import React, { FC, useState } from 'react';
import './App.css';
import { Route, Switch } from "react-router-dom";
import { useHistory } from 'react-router-dom';
import Register from './components/Register/Register';
import Login from './components/Login/Login';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
  const [userData, setUserData] = useState(null);
  const history = useHistory();

  const handleUserData = (data) => {
    console.log("data: ", data)
    setUserData(data);
  }

  if(userData){
    console.log("Logged in")
    history.push('/dashboard')
  }

  return (
      <Switch>
        <Route path="/dashboard" component={Dashboard}><Dashboard data={userData} /></Route>
        <Route path="/login"><Login onSendData={handleUserData}/></Route>
        <Route path="/register" component={Register} />
      </Switch>
  );
}

export default App;
