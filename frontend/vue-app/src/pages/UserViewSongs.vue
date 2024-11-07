<template>
    <div class="view-songs">
        <h1>{{ playlistName }}</h1>
        <ul>
            <li v-for="song in songs" :key="song.id">
                {{ song.name }} by {{ song.singer_name }}
                <button @click="deleteSong(song.id)">Delete Song</button>
            </li>
        </ul>
        <button @click="goBack">Go back</button>
    </div>
</template>

<script>
import axios from 'axios';
import router from '../router/index.js'; 

export default {
    data() {
        return {
            playlistId: this.$route.query.playlist_id,
            username: this.$route.query.username,
            playlistName: '',
            songs: [],
        };
    },
    created() {
        // console.log('Playlist ID:', this.$route.query.playlist_id); 
        console.log('Playlist Id:', this.$route.query.playlistId);
        this.fetchSongs();
    },
    methods: {
        goBack() {
            this.$router.go(-1);
        },
        async fetchSongs() {
        try {
            const response = await axios.post('/playlists/songs', {
                playlist_id: this.$route.query.playlistId,
                username: this.username
            });
            this.songs = response.data.songs;
            this.playlistName = response.data.name; // Assuming the API returns the playlist name
        } catch (error) {
            console.error('There was an error fetching the songs:', error);
        }
        },
        async deleteSong(songId) {
            try {
                await axios.post(`/playlists/${this.$route.query.playlistId}/remove-song`, { 
                    song_id: songId, username: this.username, playlist_id: this.$route.query.playlistId });
                this.songs = this.songs.filter(song => song.id !== songId);
            } catch (error) {
                console.error('There was an error deleting the song:', error);
            }
        }
    }
};
</script>

<style scoped>
/* Your CSS here */
</style>
