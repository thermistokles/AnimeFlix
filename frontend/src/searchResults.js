import React from 'react';

function SearchResults(props) {
  return (
    <div>
      <h2>Search Results</h2>
      <p>You searched for: {props.searchTerm}</p>
    </div>
  );
}

export default SearchResults;
