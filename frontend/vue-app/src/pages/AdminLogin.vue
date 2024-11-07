<template>
    <div class="admin-login">
      <center><h1 class="display-1">Administrator Login</h1></center>
      <form @submit.prevent="onSubmit">
        <div v-if="errorMsg">
          <br>
          <p class="alert alert-danger">{{ errorMsg }}</p>
        </div>
        <div class="form-group">
          <label for="adminUsername">Enter Username </label>
          <input type="text" id="adminUsername" v-model="username" class="form-control" placeholder="Username">
          <br>
        </div>
        <div class="form-group">
          <label for="adminPassword">Enter Password  </label>
          <input type="password" id="adminPassword" v-model="password" class="form-control" placeholder="Password" autocomplete="on">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
      <br>
      <h3 style="text-align: center;">Not an Admin?
        <button class="btn btn-link" @click="goBack">Go back</button>
      </h3>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Import axios
  import router from '../router/index.js';
  
  export default {
    name: "AdminLogin",
    data() {
      return {
        username: '',
        password: '',
        errorMsg: ''
      };
    },
    methods: {
      async onSubmit() {
        try {
          // Send admin credentials to backend for validation
          const response = await axios.post('http://localhost:5000/admin-login', {
            username: this.username,
            password: this.password
          });
          // Check if login was successful based on the response message
          if (response.data.message.includes('Welcome')) {
            router.push('/admin-dashboard'); // Redirect to admin dashboard
          } else {
            this.errorMsg = response.data.message; // Display error message
          }
        } catch (error) {
          console.error('Error logging in:', error);
          this.errorMsg = 'Failed to log in';
        }
      },
      goBack() {
        // Go back to the previous page
        router.go(-1);
      }
    }
  };
  </script>
  