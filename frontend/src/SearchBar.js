import React from 'react';

function SearchBar(props) {

  const handleSearchChange = (event) => {
    const searchTerm = event.target.value;
    props.onSearchChange(searchTerm);
    props.updateSearchTerm(searchTerm); // add this line
  };

  return (
    <div>
      <input type="text" placeholder="Search..." onChange={handleSearchChange}/>
      <button type="submit">Search</button>
    </div>
  );
}

export default SearchBar;