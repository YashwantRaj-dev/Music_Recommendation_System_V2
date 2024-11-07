<template>
    <div class="user-profile">
      <h1>Your Profile</h1>
      <p><strong>Name of the user:</strong> {{ username }}</p>
      <h2>Your Playlists</h2>
      <div v-for="playlist in playlists" :key="playlist.id" class="playlist">
        <p>{{ playlist.name }}</p>
        <button @click="toggleSongs(playlist.id)">View Songs</button>
        <button @click="deletePlaylist(playlist.id)">Delete Playlist</button>
        <ul v-if="visibleSongs[playlist.id]">
          <li v-for="song in playlist.songs" :key="song.id">
            {{ song.name }} by {{ song.singer_name }}
            <button @click="deleteSong(song.id, playlist.id)">Delete Song</button>
          </li>
        </ul>
      </div>
      <button @click="goBack">Go back to User Account</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Ensure axios is imported
  import router from '../router/index.js';
  export default {
    data() {
      return {
        username: '', // Assuming you fetch this from some user state or props
        playlists: [], // This would be fetched from the server
        visibleSongs: {}, // Tracks which playlists' songs are currently visible
      };
    }, 
    created() {
      this.fetchPlaylists();
      this.username = this.$route.query.username || 'Default Username';
    },
    methods: {
        goBack() {
            this.$router.go(-1);
        },
      async fetchPlaylists() {
        try {
            // Make sure to include the username in the request body
            const response = await axios.post('/playlists', {
            username: this.$route.query.username, // Include this.$route.query.username in the request 
        });
            this.playlists = response.data.playlists;
        }       
          catch (error) {
          console.error('There was an error fetching the playlists:', error);
        }
      },
      toggleSongs(playlistId) {
        // Toggle visibility of songs in a playlist
        this.$router.push({ name: 'UserViewSongs', query: { playlistId: playlistId, username: this.username }});
      },
      async deletePlaylist(playlistId) {
        try {
            await axios.delete(`/playlists/${playlistId}/delete`, { data: { username: this.username } });
            this.playlists = this.playlists.filter(playlist => playlist.id !== playlistId);
        } catch (error) {
            console.error('There was an error deleting the playlist:', error);
        }
        }, 
        async deleteSong(songId, playlistId) {
        try {
            await axios.post(`/api/playlists/${playlistId}/remove-song`, { song_id: songId, username: this.username });
            const playlistIndex = this.playlists.findIndex(playlist => playlist.id === playlistId);
            if (playlistIndex !== -1) {
            this.playlists[playlistIndex].songs = this.playlists[playlistIndex].songs.filter(song => song.id !== songId);
            }
        } 
        catch (error) {
        console.error('There was an error deleting the song:', error);
  }
}

}
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  .playlist {
    margin-bottom: 20px;
  }
  </style>
  