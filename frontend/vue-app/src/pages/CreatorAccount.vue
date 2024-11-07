<template>
  <div class="container mt-3">
    <h2>Your Creator Account</h2>

    <!-- Upload Songs Form -->
    <form @submit.prevent="uploadSong">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" class="form-control" v-model="username" placeholder="Enter your username" required>
      </div>
      <div class="form-group">
        <label for="title">Title</label>
        <input type="text" class="form-control" v-model="title" placeholder="Enter song title" required>
      </div>
      <div class="form-group">
        <label for="singer">Singer</label>
        <input type="text" class="form-control" v-model="singer" placeholder="Enter singer name" required>
      </div>
      <div class="form-group">
        <label for="album">Album</label>
        <input type="text" class="form-control" v-model="album" placeholder="Enter album name" required>
      </div>
      <div class="form-group">
        <label for="releaseDate">Release Date</label>
        <input type="date" class="form-control" v-model="releaseDateFormatted" required>
      </div>
      <div class="form-group">
        <label for="lyrics">Lyrics</label>
        <textarea class="form-control" v-model="lyrics" rows="5" placeholder="Enter song lyrics" required></textarea>
      </div>
      <div class="form-group">
        <label for="genre">Genre</label>
        <input type="text" class="form-control" v-model="genre" placeholder="Enter song genre" required> 
      </div>
      <button type="submit" class="btn btn-primary">Upload</button> 
      <div class="navigation-buttons">
      <button type="button" class="btn btn-info mt-3" @click="goToCreatorProfile">Check Your Creator Account Profile</button>
      <button @click="goBack">Go back to User Account</button>
      </div>
    </form>

    <!-- Additional UI elements and links -->
  </div>
</template>

<script>
import router from '../router/index.js';
export default {
  // props: ['username'], 
  data() {
    return {
      username: '', // Add username to the component's data
      title: '',
      singer: '',
      album: '',
      releaseDateFormatted: '', // New field to hold the formatted release date
      lyrics: '',
      genre: '',
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    }, 
    goToCreatorProfile() {
      this.$router.push({ name: 'creator-profile', query: { username: this.$route.query.username } }); // Navigate to CreatorProfile page
    },
    goBackToUserAccount() {
      this.$router.push({ name: 'login' }); // Navigate back to UserHomePage
    },
    async uploadSong() {
      // Format releaseDate in YYYY-MM-DD format
      // const formattedDate = new Date(this.releaseDateFormatted).toISOString().split('T')[0];
      // console.log('Formatted Date:', formattedDate); 
      console.log('Release Date:', this.releaseDateFormatted); 
      const username = this.username;
      const songData = {
        username: this.username,
        title: this.title,
        singer: this.singer,
        album: this.album,
        releaseDate: this.releaseDateFormatted, // Use the formatted date
        lyrics: this.lyrics,
        genre: this.genre,
      };
      
      try {
        const response = await fetch('http://localhost:5000/upload-song', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(songData),
        });
        
        const responseData = await response.json();
        if (!response.ok) {
          throw new Error(responseData.message || 'Failed to upload the song.');
        }
        alert('Song uploaded successfully.');
        // Reset form fields after successful upload
        this.username = '';
        this.title = '';
        this.singer = '';
        this.album = '';
        this.releaseDateFormatted = ''; // Reset releaseDateFormatted
        this.lyrics = '';
        this.genre = '';
      } catch (error) {
        console.error('Error:', error);
        alert(error.message);
      }
    }
  }
};
</script>

<style scoped>
/* Your styles remain the same */
</style>
