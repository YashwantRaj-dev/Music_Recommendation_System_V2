<template>
  <div class="container">
    <h2>Welcome Back To Your Personalized Home Page, {{ username }}</h2>

    <!-- <form @submit.prevent="searchSongs"> -->
      <!-- <div class="form-group">
        <label for="search_query">Search for Songs</label>
        <input type="text" class="form-control" v-model="searchQuery" placeholder="Enter song name">
      </div>
      <button type="submit" class="btn btn-primary">Search</button> -->
    <!-- </form> -->

    <div class="search-link">
      <nav>
        <a @click.prevent="navigateTo('search-songs')" style="color: orange; font-size: 16px;">Search For Songs On This Platform</a> 
      </nav>
    </div>

    <div class="search-results">
      <ul>
        <li v-for="result in searchResults" :key="result.id">
          <strong>{{ result.name }}</strong> by {{ result.artists[0].name }}
        </li>
      </ul>
    </div>

    <!-- Navigation links -->
    <div class="nav-links mt-3">
      <!-- <router-link to="/user-search" class="profile-link">Search for Songs on this Platform</router-link> | -->
      <router-link :to="{path: creatorAccountLink, query: { username: username } }" class="profile-link">Creator Account</router-link> |
      <router-link :to="{ path: '/user-profile', query: { username: username } }" class="profile-link">Profile</router-link> |
      <router-link to="/register" class="profile-link">Logout</router-link>
    </div>

    <div v-if="songInfo" class="song-info-container mt-3">
      <h3>{{ songInfo.song_name }} by {{ songInfo.artist_name }}</h3>
      <p>{{ lyrics }}</p>
    </div>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div class="genres-list mt-3">
      <h4>Genres and Songs:</h4>
      <div v-for="genreInfo in genresAndSongs" :key="genreInfo.genre">
        <h5>{{ genreInfo.genre }}</h5>
        <ul>
          <li v-for="song in genreInfo.songs" :key="song.id" class="d-flex justify-content-between align-items-center">
            <div>
              {{ song.name }} by {{ song.singer_name }}
              <!-- <router-link :to="'/read-lyrics/' + song.id" class="btn btn-info mr-2">Read Lyrics</router-link> -->
            </div>
            <div class="d-flex align-items-center">
              <!-- Pass the song ID and possibly other details as query parameters -->
              <router-link :to="{ name: 'AddToPlaylist', query: { songId: song.id, username: username } }" class="btn btn-success mr-2">Add to Playlist</router-link>
              <select v-model="songRatings[song.id]" class="form-control mr-2">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
              <button @click="rateSong(song.id)" class="btn btn-primary">Rate</button> 
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router/index.js';

export default {
data() {
  return {
    username: '', // You should set this value in your component
    searchQuery: '',
    searchResults: [],
    creatorAccountExists: false, // Initially set to false
    songInfo: null,
    lyrics: null,
    errorMessage: '',
    genresAndSongs: [],
    songRatings: {}
  };
},
mounted() {
  // Fetch creator account existence when component is mounted
  this.username = this.$route.query.username; 
  this.fetchCreatorAccountExistence();
  this.fetchGenresAndSongs();
},
methods: {
  async fetchGenresAndSongs() {
    try {
      const response = await fetch('http://localhost:5000/genres-and-songs');
      const data = await response.json();
      this.genresAndSongs = data;
    } catch (error) {
      console.error('Error fetching genres and songs:', error);
    }
  },
  async fetchCreatorAccountExistence() {
try {
  // Make a request to check if the creator account exists
  const response = await fetch('http://localhost:5000/check-creator', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username: this.username })
  });

  const data = await response.json();

  // Update creatorAccountExists based on the response
  this.creatorAccountExists = data.creatorExists;

  // Set username if the creator exists
  if (this.creatorAccountExists) {
    this.username = data.username;
  }
} catch (error) {
  console.error('Error fetching creator account existence:', error);
}
},
navigateTo(routeName) {
      // Navigate to the specified route
      this.$router.push({ name: 'SearchSongs' });
    },
  async addToPlaylist(songId) {
      try {
        // Navigate to AddToPlaylist component with the songId as parameter
        this.$router.push({ name: 'AddToPlaylist', query: { username: this.username }, params: { songId: songId } });
      } catch (error) {
        console.error('Error navigating to AddToPlaylist:', error);
      }
    },
  rateSong(songId) {
    const rating = this.songRatings[songId]; // Get the rating from the selected value

  // Send the rating data to the backend
  axios.post('/rate-song', { song_id: songId, rating: rating })
    .then(response => {
      console.log('Song rated successfully');
      // You can update any UI elements if needed
    })
    .catch(error => {
      console.error('Error rating song:', error);
    });
  }
},
computed: {
  creatorAccountLink() {
    return this.creatorAccountExists ? 'creator-account' : 'creator-registration';
  }
}
};
</script>


<style scoped>
/* Add your component-specific styles here */
</style>