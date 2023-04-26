    import axios from 'axios';
    import React, { FC, useEffect, useState } from 'react';
    import { useHistory } from 'react-router-dom';

    import './Dashboard.css'

    function Dashboard (props) {

        const history = useHistory();

        const username = JSON.parse(localStorage.getItem('username'));
        const authMethod = JSON.parse(localStorage.getItem('authMethod'));
        const isOver18 = JSON.parse(localStorage.getItem('isOver18'));
        const genres = JSON.parse(localStorage.getItem('genres'));
        const movieShow = JSON.parse(localStorage.getItem('movieShow'));

        const [data, setData] = useState({genres : genres, isOver18: isOver18, movieShow})
        const [userData, setuserData]  = useState({username : username})

        const [recommendedUserAnimes, setRecommendedUserAnimes] = useState([]);
        const [neuralNetworkRecommendations, setNeuralNetworkRecommendations] = useState([]);

        const [isModalVisible, setIsModalVisible] = useState(false);
        const [tempAnime, setTempAnime] = useState('');
        const [clickedAnime, setClickedAnime]=useState([]);

        useEffect(() => {
            const fetchRecommendedUserAnimes = async () => {
                if(authMethod == "login"){
                    axios.post('http://127.0.0.1:5000/existingUserData', userData)
                    .then(response => {
                        setRecommendedUserAnimes(response.data)
                        
                    })
                    .catch(error => {
                        console.error(error);
                    });
                }
                else if(authMethod == "register"){
                    console.log("register")
            
                    axios.post('http://127.0.0.1:5000/newUserData', data)
                    .then(response => {
                        setRecommendedUserAnimes(response.data)
                    })
                    .catch(error => {
                        console.error(error);
                    });
                }
                else{
                    history.push("/")
                }

                const fetchNeuralNetworkRecommendations = async () => {
                    axios.post('http://127.0.0.1:5000/topRatedRecommendations', userData)
                    .then(response => {
                        setNeuralNetworkRecommendations(response.data)
                        
                    })
                    .catch(error => {
                        console.error(error);
                    });
                };
                
                fetchNeuralNetworkRecommendations();
            };
        
            fetchRecommendedUserAnimes();
        }, []);

        const handleLogoutClick = () => {
            localStorage.clear()
            history.push('/');
        }

        const [profileData] = useState(null)
    const [userBasedCFResults, setUserBasedCFResults] = useState([]);


    const [searchText, setSearchText] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const handleSearch = () => {
        axios
        .post("http://127.0.0.1:5000/search", {searchText})
        .then((response) => {
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

    const handleImageClick = (anime) => {
        setClickedAnime(anime.title);
        setTempAnime(anime.title);
        console.log(anime.title);
        setIsModalVisible(true);
      };
    
      useEffect(() => {
        if (clickedAnime !== null) {
          axios
          .post("http://127.0.0.1:5000/content", { clickedAnime })
          .then((response) => {
            console.log(response.data);
            //setSearchResults_content(response.data);
            setClickedAnime(response.data);
          })
          .catch((error) => {
            console.error(error);
          });
        }
    
      }, [clickedAnime]);


        return(
            <div>
                <h1>Welcome {username}</h1>

                <div>
            <label>
            <input type="text" placeholder="Search..." name='animeName'  value = {searchText}
            onChange={(e)=>setSearchText(e.target.value)}
            />
            </label>
            <button onClick={handleSearch}>Search</button> 
            <div key={Date.now()} className="anime-container">
    {searchResults.map((anime) => (
        <div key={anime.anime_id} className="recommended-anime-card">
            <a onClick={() => handleImageClick(anime)}>
        <img src={anime.img_url} alt={anime.title} className="anime-img" />
        </a>
        <div className="anime-title">
            <p href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</p>
        </div>
        </div>
    ))}
    </div>
    </div>
                {isModalVisible && clickedAnime && (
  <div className="box" style={{ border: '1px solid black' }}>
    <h3>Because you watched {tempAnime}</h3>
    <div key={Date.now()} className="anime-container">
      {Array.isArray(clickedAnime) && clickedAnime.map((anime) => (
        <div className="recommended-anime-card">
          <img src={anime.image_url} alt={anime.title} className="anime-img" />
          <div className="anime-title">
            <p href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</p>
          </div>
        </div>
      ))}
    </div>
  </div>
)}

<br></br>

                <div>
            <h3>Here are our recommendations for you!</h3>
            <div key={Date.now()} className="anime-container">
    {recommendedUserAnimes.map((anime) => (
        <div key={anime.anime_id} className="recommended-anime-card">
         <a onClick={() => handleImageClick(anime)}>
        <img src={anime.img_url} alt={anime.title} className="anime-img" />
        </a>
        <div className="recommended-anime-title">
            <p href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</p>
        </div>
        </div>
    ))}
    </div>

        </div>

        <br></br>

        <div>
            {authMethod === "login" &&
                <div>
                <h3>Top rated Anime</h3>
                <div>
                <div key={Date.now()} className="recommended-anime-container">
                    {neuralNetworkRecommendations.map((anime) => (
                    <div key={anime.anime_id} className="recommended-anime-card">
                        <a onClick={() => handleImageClick(anime)}>
                    <img src={anime.img_url} alt={anime.title} className="anime-img" />
                    </a>
                        <div className="recommended-anime-title">
                        <p href={anime.link} target="_blank" rel="noopener noreferrer">{anime.title}</p>
                        </div>
                    </div>
                    ))}
                </div>
                </div>
                </div>
            }
        </div>

        <br></br>

        <button onClick={handleLogoutClick}>Logout</button>
        
            </div>
            
        )
    }

    export default Dashboard;