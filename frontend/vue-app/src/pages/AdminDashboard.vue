<template>
  <div class="container mt-5">
    <h2>Administrator Dashboard</h2>
    <!-- Display additional information -->
    <div class="row">
      <div class="col-md-3">
        <h3>Total Number of Users: {{ totalUsers }}</h3>
      </div>
      <div class="col-md-3">
        <h3>Total Number of Creators: {{ totalCreators }}</h3>
      </div>
      <div class="col-md-3">
        <h3>Total Number of Songs: {{ totalSongs }}</h3>
      </div>
      <div class="col-md-3">
        <h3>Average Ratings of All Songs: {{ averageRatingAllSongs }}</h3>
      </div>
    </div>

    <!-- Existing content for creators, genres, and songs -->
    <!-- ... -->

    <div>
    <h1>List of Creators</h1>
    <ul>
      <li v-for="creator in creators" :key="creator.id">
        {{ creator.username }}
        <button @click="removeCreator(creator.id)">Remove</button>
      </li>
    </ul>
    </div>

      <div class="col-md-6">
        <h3>List of Genres</h3>
        <ul class="list-group">
          <li v-for="(genre, index) in genres" :key="index" class="list-group-item">{{ genre }}</li>
        </ul>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-12">
        <h3>List of Songs</h3>
        <ul class="list-group">
          <li v-for="(song, index) in songs" :key="index" class="list-group-item">
            {{ song.name }} 
            <button class="btn btn-primary" @click="viewLyrics(index)">View Lyrics</button>
            <button class="btn btn-danger" @click="deleteSong(song.id)">Delete</button>
            <!-- Display lyrics -->
            <div v-if="selectedSongIndex === index">
              <p>{{ selectedSongLyrics }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Logout button -->
    <div class="row mt-4">
      <div class="col-md-12">
        <router-link to="/register" class="btn btn-primary">Logout</router-link>
      </div>
    </div>
    <!-- ... -->
  
</template>

<script>
import axios from 'axios';
import router from '../router/index.js';

export default {
  data() {
    return {
      totalUsers: 0,
      totalCreators: 0,
      totalSongs: 0,
      averageRatingAllSongs: 0,
      creators: [],
      genres: [],
      songs: [],
      selectedSongIndex: null,
      selectedSongLyrics: ''
    };
  },
  mounted() {
    this.fetchDashboardData();
    this.fetchSongs();
  },
  methods: {
    fetchDashboardData() {
      axios.get('/admin/dashboard')
        .then(response => {
          this.totalUsers = response.data.totalUsers;
          this.totalCreators = response.data.totalCreators;
          this.totalSongs = response.data.totalSongs;
          this.averageRatingAllSongs = response.data.averageRatingAllSongs;
          this.creators = response.data.creators;
          this.genres = response.data.genres;
        })
        .catch(error => {
          console.error('Error fetching dashboard data:', error);
        });
    },
    fetchSongs() {
      axios.get('/admin/songs')
        .then(response => {
          this.songs = response.data.songs;
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
        });
    },
    viewLyrics(index) {
      const songId = this.songs[index].id;
      axios.post('/fetch-song-lyrics', { songId: songId })
        .then(response => {
          // Display lyrics of the selected song
          this.selectedSongLyrics = response.data.lyrics;
          this.selectedSongIndex = index;
          console.log(response.data.lyrics);
          // Here you can update your UI to display the lyrics
        })
        .catch(error => {
          console.error('Error fetching lyrics:', error);
        });
    },
    deleteSong(songId) {
      // Implement logic to delete the selected song
      axios.delete(`/songs/${songId}`)
        .then(response => {
          // Handle successful deletion
          console.log('Song deleted successfully');
          // Refresh songs after deletion
          this.fetchSongs();
        })
        .catch(error => {
          console.error('Error deleting song:', error);
        });
    },
    removeCreator(creatorId) {
      axios.post('/remove_creator', { creator_id: creatorId })
        .then(response => {
          console.log('Creator and associated data removed successfully');
          // Refresh dashboard data after deletion
          this.fetchDashboardData();
        })
        .catch(error => {
          console.error('Error removing creator:', error);
        });
    }
  }
};
</script>


