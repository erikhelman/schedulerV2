<template>
  <b-row class="justify-content-center">
    <b-col cols="4">
      <b-card 
        :style="{ 'marginTop': '30vh' }"
        header="Login"
        header-text-variant="white"
        header-bg-variant="dark">
        <b-form @submit.prevent="onSubmit">
          <b-form-group
              label="Email Address:"
              label-for="emailAddress">
              <b-form-input id="emailAddress"
                :v-model="email">
              </b-form-input>
          </b-form-group>
          <b-form-group
              label="Password:"
              label-for="password">
              <b-form-input id="password"
                :v-model="email">
              </b-form-input>
          </b-form-group>
        </b-form>
        <b-button
        variant="secondary">
        Sign In
        </b-button>
        <b-row class="justify-content-center">
        <b-link :to="{ name: 'register' }">New User? Register here</b-link> 
        </b-row>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  export default {
    data() {
      return {
        email: '',
        password: '',
        loading: false
      }
    }
  }
</script>

<style scoped>

</style>
