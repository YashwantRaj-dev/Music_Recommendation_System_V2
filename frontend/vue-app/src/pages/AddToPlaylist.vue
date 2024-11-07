<template>
    <div class="add-to-playlist">
      <h2>Add to Playlist</h2>
      
      <ul>
        <li v-for="playlist in playlists" :key="playlist.id">
          {{ playlist.name }}
          <button @click="addToPlaylist(playlist.id)">Add</button>
        </li>
      </ul>
      <h3>Create New Playlist</h3>
      <input type="text" v-model="username" placeholder="Enter your username">
      <input type="text" v-model="newPlaylistName" placeholder="Enter playlist name">
      <button @click="createNewPlaylist">Create</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import router from '../router/index.js';
  
  export default {
    data() {
      return {
        playlists: [],
        newPlaylistName: '',
        username: '',
        songId: null
      };
    },
    created() {
      this.fetchPlaylists();
      this.songId = this.$route.query.songId;
    },
    methods: {
      async fetchPlaylists() { 
        try {
        // Update to check for username in query if not set in data
        const currentUsername = this.username || this.$route.query.username;
        console.log('Fetching playlists for:', currentUsername);
        const response = await axios.post('http://localhost:5000/playlists', {
        username: currentUsername
        });
        this.playlists = response.data.playlists;
        // alert("Song added to playlist successfully");
        } catch (error) {
            console.error('Error fetching playlists:', error.response);
            }
        },
      async addToPlaylist(playlistId) {
        try {
          const currentUsername = this.username || this.$route.query.username; 
          await axios.post(`/playlists/${playlistId}/add-song`, {
            username: currentUsername, 
            song_id: this.songId
          });
          this.$router.go(-1); // Optionally, redirect the user back to the previous page
        } catch (error) {
            if (error.response && error.response.status === 409) {
                alert(error.response.data.message);
            } 
            else {
                console.error('Error adding song to playlist:', error);
            }
        }
      },
      async createNewPlaylist() {
        try {
          const response = await axios.post('/playlists/create', {
            username: this.username,
            name: this.newPlaylistName
          });
          const newPlaylistId = response.data.playlist_id;
          this.playlists.push({ id: newPlaylistId, name: this.newPlaylistName });
          this.addToPlaylist(newPlaylistId); // Add the song to the newly created playlist
        } catch (error) {
          console.error('Error creating playlist:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Your styles here */
  </style>
  