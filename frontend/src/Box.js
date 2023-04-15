import React from 'react';

function Box(props) {
  return (
    <div className="box" style={{ border: '1px solid black' }}>
      <h2>{props.title}</h2>
      <p>{props.content}</p>
    </div>
  );
}

export default Box;
