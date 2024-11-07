<template>
    <div class="greetings">
      <h1 class="green">Hello Shark</h1>
      <router-link :to="{ name: 'register' }">Go to Register</router-link>
    </div>
  </template>
  
  
  
  <script>
    export default {
      name: 'Shark'
    }
  </script>
  