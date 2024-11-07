<template>
    <div class="container mt-3">
      <h2>Creator Account</h2>
      <nav>
        <a @click.prevent="navigateTo('creator-account')" style="color: green; font-size: 16px;">Upload Song</a> | 
        <a @click.prevent="navigateTo('login')" style="color: green; font-size: 16px;">User Account</a> | 
        <a @click.prevent="logout" style="color: green; font-size: 16px;">Logout</a>
      </nav>
      <h3 class="mt-4">Dashboard</h3>
      <div class="dashboard-info">
        <div class="box">
          <h4>Total Songs Uploaded</h4>
          <!-- Placeholder for total songs -->
          <p>{{ totalSongs }}</p>
        </div>
        <div class="box">
          <h4>Average Rating</h4>
          <!-- Placeholder for average rating -->
          <p>{{ averageRating }}</p>
        </div>
        <div class="box">
          <h4>Total Albums</h4>
          <!-- Placeholder for total albums -->
          <p>{{ totalAlbums }}</p>
        </div>
      </div>
      <h3>Your Uploads</h3>
      <div v-for="album in albums" :key="album.id" class="album-entry">
        <p>{{ album.name }}</p>
        <button @click="viewSongs(album.id)">View Songs</button>
        <button @click="deleteAlbum(album.id)">Delete</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import router from '../router/index.js';
  export default {
    data() {
      return {
        totalSongs: 0,
        averageRating: 0,
        totalAlbums: 0,
        albums: []
      };
    },
    methods: {
        navigateTo(routeName) {
            if (routeName === 'creator-account') {
                this.$router.go(-1); // Go back one page
            } else if (routeName === 'login') {
                this.$router.go(-2); // Go back two pages
            }
        },
      logout() {
        this.$router.push({ name: 'register' });
      },
      viewSongs(albumId) {
        this.$router.push({ name: 'CreatorViewSongs', query: { albumId: albumId, username: this.$route.query.username } });
      },
      async deleteAlbum(albumId) {
        try {
            const response = await axios.delete(`/albums/${albumId}`, { data: { username: this.$route.query.username } });
            if (response.status === 200) {
            // Remove the album from the local albums array or refresh the list
            // Example: Refreshing the list
            this.fetchCreatorData(this.$route.query.username);
            alert('Album deleted successfully.');
            } else {
            alert('Failed to delete album.');
            }
        } catch (error) {
            console.error('Error deleting album:', error);
            alert('Failed to delete album.');
        }
        },
      async fetchCreatorData(username) {
        try {
                const response = await axios.post('/creator/dashboard', { username: this.$route.query.username });
                this.totalSongs = response.data.totalSongs;
                this.averageRating = response.data.averageRating;
                this.totalAlbums = response.data.totalAlbums;
                this.albums = response.data.albums;
            } catch (error) {
                console.error('Error fetching creator data:', error);
            }
        }
    },
    created() {
      console.log('Username:', this.$route.query.username);
      const username = this.$route.query.username;  
      this.fetchCreatorData(username);
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  .box {
    margin-bottom: 20px;
  }
  </style>
  