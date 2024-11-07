<template>
    <div class="container">
      <h2>Search for Songs</h2>
        
      <form @submit.prevent="searchSongs">
        <div class="form-group">
          <label for="searchByName">By Name </label>
          <input type="text" id="searchByName" v-model="searchByName" class="form-control" placeholder="Enter song name">
        </div>
          
        <div class="form-group">
          <label for="searchByRating">By Rating </label>
          <input type="number" id="searchByRating" v-model="searchByRating" class="form-control" min="1" max="5" placeholder="Enter rating (1-5)">
        </div>
          
        <div class="form-group">
          <label for="searchByGenre">By Genre </label>
          <input type="text" id="searchByGenre" v-model="searchByGenre" class="form-control" placeholder="Enter genre">
        </div>
          
        <div class="form-group">
          <label for="searchByAlbum">By Album </label>
          <input type="text" id="searchByAlbum" v-model="searchByAlbum" class="form-control" placeholder="Enter album name">
        </div>
          
        <button type="submit" class="btn btn-primary">Submit</button>
        <button type="button" class="btn btn-secondary" @click="goBack">Go Back</button>
      </form>
        
      <!-- Display search results -->
      <div v-if="searchResults.length > 0" class="mt-4">
        <h3>Search Results:</h3>
        <ul>
          <li v-for="song in searchResults" :key="song.id">
            {{ song.name }} - {{ song.singer_name }}
          </li>
        </ul>
      </div>
      <div v-else-if="searchPerformed && searchResults.length === 0" class="mt-4">
        <p>No songs found with the given criteria.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchByName: '',
        searchByRating: '',
        searchByGenre: '',
        searchByAlbum: '',
        searchResults: [],
        searchPerformed: false
      };
    },
    methods: {
      searchSongs() {
        // Clear previous search results
        this.searchResults = [];
        
        // Prepare the search data
        const searchData = {
          name: this.searchByName,
          rating: this.searchByRating,
          genre: this.searchByGenre,
          album: this.searchByAlbum
        };
  
        // Make a POST request to the backend for each search criterion
        if (this.searchByName) {
          axios.post('/search-by-name', searchData)
            .then(response => {
              // Handle the response
              console.log('Search results:', response.data);
              this.searchResults = response.data.songs; // Update searchResults with the songs
              this.searchPerformed = true; // Set searchPerformed flag to true
            })
            .catch(error => {
              // Handle errors
              console.error('Error searching for songs:', error);
            });
        } else if (this.searchByRating) {
          axios.post('/search-by-rating', searchData)
            .then(response => {
              console.log('Search results by rating:', response.data);
              this.searchResults = response.data.songs;
              this.searchPerformed = true;
            })
            .catch(error => {
              console.error('Error searching by rating:', error);
            });
        } else if (this.searchByGenre) {
          axios.post('/search-by-genre', searchData)
            .then(response => {
              console.log('Search results by genre:', response.data);
              this.searchResults = response.data.songs;
              this.searchPerformed = true;
            })
            .catch(error => {
              console.error('Error searching by genre:', error);
            });
        } else if (this.searchByAlbum) {
          axios.post('/search-by-album', searchData)
            .then(response => {
              console.log('Search results by album:', response.data);
              this.searchResults = response.data.songs;
              this.searchPerformed = true;
            })
            .catch(error => {
              console.error('Error searching by album:', error);
            });
        }
      },
      goBack() {
        // Navigate back to the previous page
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  