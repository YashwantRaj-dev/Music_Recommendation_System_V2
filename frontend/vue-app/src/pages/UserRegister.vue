<template>
  <div class="main-form">
      <center><h1 class="display-1">Register Yourself</h1></center>
      <form @submit.prevent="onSubmit">
          <div v-if="errorMsg">
              <br>
              <p class="alert alert-danger" > {{errorMsg}}</p>
          </div>
          <input class="form-control" type="text" v-model="username" placeholder="Username" >
          <br>
          <input class="form-control" type="password" v-model="password" placeholder="Password" autocomplete="on">
          <br>
          <input class="form-control" type="password" v-model="confirmPassword" placeholder="Confirm Password" autocomplete="on">
          <br>
          <button class="form-control btn btn-primary" type="submit" >Submit</button>
      </form>
      <br>
      <h3 style="text-align: center;">Already have an account? Login please!!  
          <router-link class="nav-link" to="/login">Click here to Login</router-link>
      </h3>
      <h3 style="text-align: center;">Admin? Login here instead!
          <router-link class="nav-link" to="/admin-login">Click here to Login as Admin</router-link>
      </h3>
  </div>
</template>

<script>
import router from '../router/index.js';

export default {
  name: "UserRegister",
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      errorMsg: ''
    };
  },
  methods: {
    async onSubmit() {
      if (this.password !== this.confirmPassword) {
        this.errorMsg = 'Passwords do not match';
        return;
      } 
      try {
        const response = await fetch('http://localhost:5000/register-validation', {
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
          console.log(data,234);
          router.push('/login');
        } else {
          console.error('Registration Error:', data.message);
          this.errorMsg = data.message;
        }
      } catch (error) {
        console.error('Error:', error);
        this.errorMsg = 'An error occurred during registration';
      }
    }
  }
};
</script>

<style scoped>
  .main-form{
      margin-left: 25%; 
      margin-right: 25%;
  }
</style>
