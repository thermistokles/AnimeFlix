//import SearchBar from './SearchBar';
import TextBlock from './TextBlock';
import Box from './Box';
// import SmallBox from './SmallBox';
import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
function App(){

  const [recommendedAnimes, setRecommendedAnimes] = useState([]);

  // useEffect(() => {
  //   axios
  //     .get('/recommendations')
  //     .then((response) => {
  //       setRecommendations(response.data);
  //     })
  //     .catch((error) => {
  //       console.error(error);
  //     });
  // }, []);
  useEffect(() => {
    const fetchRecommendedAnimes = async () => {
      try {
        const response = await axios.get('/recommendations');
        setRecommendedAnimes(response.data);
      } catch (error) {
        console.error(error);
      }
    };
  
    fetchRecommendedAnimes();
  }, []);
  
  // const [userRecommendations, setUserRecommendations] = useState([]);
  // const [searchText, setSearchText] = useState('')
  const [profileData] = useState(null)
  const [userBasedCFResults, setUserBasedCFResults] = useState([]);


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
<div>
        <h2>User Based CF</h2>
        <div key={Date.now()} className="recommended-anime-container">
  {recommendedAnimes.map((anime) => (
    <div key={anime.anime_id} className="recommended-anime-card">
      <img src={anime.img_url} alt={anime.title} className="recommended-anime-img" />
      <div className="recommended-anime-title">
        <a href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</a>
      </div>
    </div>
  ))}
</div>

      </div>

      <Box title="Item Based CF" content="This is the content for box 2."/>
      <Box title="Content Based" content="This is the content for box 3."/>
      {/* Add the rest of your components here */}
    </div>
  );
}

export default App;