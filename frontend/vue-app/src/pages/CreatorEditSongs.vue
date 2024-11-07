<template>
    <div class="container mt-3">
      <h2>Edit Song</h2>
      <form @submit.prevent="updateSong">
        <div class="form-group">
          <label for="title">Title</label>
          <input type="text" class="form-control" v-model="title" placeholder="Enter song title" required>
        </div>
        <div class="form-group">
          <label for="singer">Singer</label>
          <input type="text" class="form-control" v-model="singer" placeholder="Enter singer name" required>
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
        <button @click="goBack">Go back</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import router from '../router/index.js';
  
  export default {
    data() {
      return {
        title: '',
        singer: '',
        releaseDateFormatted: '',
        lyrics: '',
        genre: ''
      };
    },
    created() {
      // Retrieve song details from route query
      this.songId = this.$route.query.songId; 
      this.fetchSongDetails(this.songId);
    },
    methods: {
      fetchSongDetails(songId) {
        // Make API call to fetch song details based on songId
        axios.post('/fetch-song-details', { songId }) 
          .then(response => {
            const song = response.data.song;
            this.title = song.title;
            this.singer = song.singer;
            this.releaseDateFormatted = song.releaseDate;
            this.lyrics = song.lyrics;
            this.genre = song.genre;
          })
          .catch(error => {
            console.error('Error fetching song details:', error);
          });
      },
      updateSong() {
        // Make API call to update song details
        const updatedSongData = {
          songId: this.songId,
          title: this.title,
          singer: this.singer,
          releaseDate: this.releaseDateFormatted,
          lyrics: this.lyrics,
          genre: this.genre
        };
  
        axios.post('/update-song', updatedSongData)
          .then(response => {
            console.log(response.data.message);
            // Redirect to CreatorViewSongs.vue after successful update
            // router.push({ name: 'CreatorViewSongs' });
            this.$router.go(-1);
          })
          .catch(error => {
            console.error('Error updating song:', error);
          });
      },
      goBack() {
        // Navigate back to CreatorViewSongs.vue
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Your styles remain the same */
  </style>
  