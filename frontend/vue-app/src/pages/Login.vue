<template>
    <div>
      <h1>Login Page</h1>
      <form @submit.prevent="login"> <!-- Add @submit.prevent here -->
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="formData.username">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="formData.password">
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import router from '../router/index.js'; 
  export default {
    data() {
      return {
        formData: {
          username: '',
          password: ''
        } 
      };
    },
    methods: { 
      // In Login.vue, modify the login method
      async login() {
  try {
    const response = await fetch('http://localhost:5000/login-validation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.formData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data.message);
      console.log('Received username:', data.username);
      // Pass the username as a query parameter
      this.$router.push({ name: 'user-home', query: { username: this.formData.username } });
    } else {
      console.error('Error:', response.statusText);
    }
  } catch (error) { 
    console.error('Error:', error);
  }
}


    }
  }
  </script>
  