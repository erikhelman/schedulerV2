<template>
<b-container fluid>
  <router-view></router-view>
</b-container>
  
</template>

<script>
// @ is an alias to /src
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";

export default {
  name: 'app',
  components: {
    'app-login': Login,
    'app-register': Register
  }
}
</script>

<style>

</style>
