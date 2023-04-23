import { useState } from 'react';
import axios from 'axios';

const SearchBar = (props) => {

  const [searchText, setSearchText] = useState('')
  
  const handleSearch=()=>{
  axios.post('/search', { searchText })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
}

return (
  <form>
  <div>
    <label>
      Anime:
      <input type="text" placeholder="Search..." name='animeName'  value = {searchText}
      onChange={(e)=>setSearchText(e.target.value)}
      />
    </label>
    <button onClick={handleSearch}>Search</button> 
  </div>
  </form>
)

}

export default SearchBar;