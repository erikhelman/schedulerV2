import Vue from "vue";
import Router from "vue-router";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import Success from "./components/Success.vue";

Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: Login },
  { path: '/register',name: 'register', component: Register },
  { path: '/success', name: 'success', component: Success }
]

export default new Router({mode: 'history', routes })