<template>
    <div class="container mt-3">
      <h2>Register as a CREATOR</h2>
  
      <!-- Creator registration form -->
      <form @submit.prevent="registerCreator">
        <div class="form-group">
          <label for="username">Enter Your Username</label>
          <input type="text" class="form-control" id="username" v-model="username" placeholder="Username" required>
        </div>
        <div class="form-group">
          <label for="password">Enter Your Password</label>
          <input type="password" class="form-control" id="password" v-model="password" placeholder="Password" required>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
  
      <!-- Navigation links -->
      <div class="nav-links mt-3">
        <!-- Replace with a button or link that triggers logout method -->
        <router-link to="/user-home" class="profile-link">Back to User Account</router-link> |
        <router-link to="/logout" class="profile-link">Logout</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import router from '../router/index.js';
  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async registerCreator() {
        try {
          const response = await fetch('http://localhost:5000/register-creator', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
          const data = await response.json();
          if (response.ok) {
            console.log('Creator registered successfully:', data.message);
            // Redirect to CreatorAccount.vue upon successful registration
            router.push('/creator-account');
          } else {
            console.error('Registration Error:', data.message);
            // Handle registration error
          }
        } catch (error) {
          console.error('Error registering creator:', error);
          // Handle registration error
        }
      },
      logout() {
        // Here, add any logout logic, like clearing local storage or tokens
        console.log('User logged out.');
        // Redirect to UserRegistrationPage
        router.push('/register');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Your styles here */
  </style>
  