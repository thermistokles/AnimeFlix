import React from 'react';

function SmallBox(props) {
  return (
    <div className="small-box" style={{ backgroundColor: props.color,border: '1px solid black' }}>
      <p>{props.content}</p>
    </div>
  );
}

export default SmallBox;