<template>
    <div class="container mt-3">
      <div style="color: orangered; font-size: 16px;">
        Album: {{ albumName }} | <span @click="goBack">Go Back</span>  
      </div>
      <h2>{{ albumName }}</h2>
      <div v-for="song in songs" :key="song.id" class="song-entry">
        <p>{{ song.name }} - {{ song.singer_name }}</p>
        <button @click="editSong(song)">Edit</button>
        <button @click="deleteSong(song.id)">Delete</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import router from '../router/index.js';
  
  export default {
    data() {
      return {
        albumName: '',
        songs: [],
      };
    },
    methods: {
      async fetchAlbumSongs(albumId, username) {
        try {
          const response = await axios.post('/albums/songs', { album_id: albumId, username });
          this.albumName = response.data.name;
          this.songs = response.data.songs;
        } catch (error) {
          console.error('Error fetching album songs:', error);     
          if (error.response) {
            console.error('Server Error:', error.response.data);
          } else if (error.request) {
            console.error('Request Error:', error.request);
          } else {
            console.error('Error:', error.message);
          }
        }
      },
      editSong(song) {
        // Logic to navigate to song edit page with songId
        this.$router.push({ name: 'CreatorEditSongs', query: { songId: song.id, songDetails: JSON.stringify(song) } });
      },
      deleteSong(songId) {
        // Logic to delete the song with songId
        // Send a request to delete the song
        axios.delete(`/songs/${songId}`)
          .then(response => {
            console.log(response.data.message);
            this.$router.go(-1);
            // Assuming you want to update the list of songs after deletion, you can fetch the updated list
            // this.fetchAlbumSongs(this.$route.query.albumId, this.$route.query.username);
          })
          .catch(error => {
            console.error('Error deleting song:', error);
          });
      },
      goBack() {
        // Navigate back to the previous page
        this.$router.go(-1);
      },
    },
    created() {
      const albumId = this.$route.query.albumId;
      const username = this.$route.query.username;
      this.fetchAlbumSongs(albumId, username);
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  .song-entry {
    margin-bottom: 10px;
  }
  </style>
  