import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Shark from '../pages/Shark.vue'
import Login from '../pages/Login.vue'
import UserRegister from '../pages/UserRegister.vue'
import UserHomePage from '../pages/UserHomePage.vue'
import CreatorRegistration from '../pages/CreatorRegistration.vue'
import CreatorAccount from '../pages/CreatorAccount.vue'
import CreatorProfile from '../pages/CreatorProfile.vue'
import UserProfile from '../pages/UserProfile.vue'
import AddToPlaylist from '../pages/AddToPlaylist.vue'
import UserViewSongs from '../pages/UserViewSongs.vue';
import CreatorViewSongs from '../pages/CreatorViewSongs.vue';
import CreatorEditSongs from '../pages/CreatorEditSongs.vue';
import SearchSongs from '../pages/SearchSongs.vue';
import AdminLogin from '../pages/AdminLogin.vue';
import AdminDashboard from '../pages/AdminDashboard.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView 
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/shark',
      name: 'shark', // Unique name for the shark route
      component: Shark
    },
    {
      path: '/login', // Define the path for the login page
      name: 'login', // Unique name for the login route
      component: Login // Assign the Login component
    }, 
    {
      path: '/register', // Define the path for the register page
      name: 'register', // Unique name for the login route
      component: UserRegister // Assign the Login component
    },
    {
      path: '/user-home', // Define the path for the user home page
      name: 'user-home', // Unique name for the user home route
      component: UserHomePage // Assign the home component
    },
    {
      path: '/creator-registration', 
      name: 'creator-registration', 
      component: CreatorRegistration 
    },
    {
      path: '/creator-account', 
      name: 'creator-account', 
      component: CreatorAccount 
    },
    {
      path: '/creator-profile',
      name: 'creator-profile',
      component: CreatorProfile
    },
    {
      path: '/user-profile',
      name: 'user-profile',
      component: UserProfile
    },
    {
      path: '/add-to-playlist',
      name: 'AddToPlaylist',
      component: AddToPlaylist
    },
    {
      path: '/user-view-songs',
      name: 'UserViewSongs',
      component: UserViewSongs
    },
    {
      path: '/creator-view-songs',
      name: 'CreatorViewSongs',
      component: CreatorViewSongs
    },
    {
      path: '/creator-edit-songs',
      name: 'CreatorEditSongs',
      component: CreatorEditSongs
    },
    {
      path: '/search-songs',
      name: 'SearchSongs',
      component: SearchSongs
    },
    {
      path: '/admin-login',
      name: 'AdminLogin',
      component: AdminLogin
    },
    {
      path: '/admin-dashboard',
      name: 'AdminDashboard',
      component: AdminDashboard
    }
    
  ]
})

export default router
