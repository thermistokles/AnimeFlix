//import SearchBar from './SearchBar';
import TextBlock from './TextBlock';
import Box from './Box';
import SmallBox from './SmallBox';
import { useState } from 'react';
import axios from 'axios';
import './App.css';
function App(){

  // const [searchText, setSearchText] = useState('')
  const [profileData] = useState(null)

  // useEffect(() => {
  //   const getData = async () => {
  //     try {
  //       const response = await axios.get('/ucf');
  //       setProfileData(response.data);
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   };

  //   getData();
  // }, []);
  
  // const handleSearch = () => {
  //   console.log(searchText);
  //   axios.post(
  //     '/search',
  //     { searchText },
  //     //{ headers: { 'Content-Type': 'application/json' } } // Add this line
  //   )
  //     .then(response => {
  //       console.log("from flask->");
  //       console.log(response.data);
  //     })
  //     .catch(error => {
  //       console.error(error);
  //     });
  // };

  const [searchText, setSearchText] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = () => {
    console.log(searchText);
    axios
      .post("/", { searchText })
      .then((response) => {
        console.log("from flask->");
        console.log(response.data);
  
        // Filter unique anime titles
        const uniqueTitles = new Set();
        const uniqueResults = response.data.filter((anime) => {
          if (uniqueTitles.has(anime.title)) {
            return false;
          } else {
            uniqueTitles.add(anime.title);
            return true;
          }
        });
  
        setSearchResults(uniqueResults);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div>
      <TextBlock />
      <div>
        <label>
        Anime:
        <input type="text" placeholder="Search..." name='animeName'  value = {searchText}
        onChange={(e)=>setSearchText(e.target.value)}
        />
        </label>
        <button onClick={handleSearch}>Search</button> 
        <div key={Date.now()} className="anime-container">
  {searchResults.map((anime) => (
    <div key={anime.anime_id} className="anime-card">
      <img src={anime.img_url} alt={anime.title} className="anime-img" />
      <div className="anime-title">
        <a href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</a>
      </div>
    </div>
  ))}
</div>
      </div>
      
      {profileData && (
        <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me: {profileData.about_me}</p>
        </div>
      )}

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