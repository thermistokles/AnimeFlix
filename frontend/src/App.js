import SearchBar from './SearchBar';
import TextBlock from './TextBlock';
import Box from './Box';
import SmallBox from './SmallBox';
import React, { useState } from 'react';
import SearchResults from './searchResults';

function App() {

  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (value) => {
    setSearchTerm(value);
  };

  const updateSearchTerm = (value) => {
    setSearchTerm(value);
  };

  return (
    <div>
      <TextBlock />
      <SearchBar onSearchChange={handleSearchChange} updateSearchTerm={updateSearchTerm} />
      <SearchResults searchTerm={searchTerm} />
      <Box title="User Based CF" content="This is the content for box 1.">
        <SmallBox color="red" content="1" />
        <SmallBox color="green" content="2" />
        <SmallBox color="blue" content="3" />
      </Box>
      <Box title="Item Based CF" content="This is the content for box 2."/>
      <Box title="Content Based" content="This is the content for box 3."/>
      {/* Add the rest of your components here */}
    </div>
  );
}

export default App;
