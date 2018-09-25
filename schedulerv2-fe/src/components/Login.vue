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
              label-for="email">
              <b-form-input id="email"
                :state="(errors.email) ? false : null"
                maxLength="50"
                v-model="email">
              </b-form-input>
              <b-form-invalid-feedback>
                  Please enter a valid email address
              </b-form-invalid-feedback>
          </b-form-group>          
          <b-form-group
              label="Password:"
              label-for="password">
              <b-form-input id="password"
                type="password"
                maxLength="100"
                v-model="password"
                :state="(errors.password) ? false : null">
              </b-form-input>
              <b-form-invalid-feedback>
                Please enter your password
              </b-form-invalid-feedback>
          </b-form-group>
        </b-form>
                <b-alert 
          :style="{marginTop: '1em'}"
          :show="showAlert"
          variant="danger">
          {{ errors.loginError }}
        </b-alert>
        <b-button
          variant="secondary"
          @click="onSubmit">
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
import axios from 'axios';
import { required, email, minLength } from 'vuelidate/lib/validators';

export default {
  data() {
    return {
      email: '',
      password: '',
      loginState: false,
      errors: {},
      showAlert: false
    }
  },
    validations: {
    email: {
      required,
      email            
    },
    password: {
      required,
      minLength: minLength(1)
    }
  },
  methods: {
    validateForm() {

          this.errors = {};

          if (this.$v.$invalid) {
              this.errors.email = (this.$v.email.$invalid) ? true : null;
              this.errors.password = (this.$v.password.$invalid) ? true : null;

              return false;
          } else {
              return true;
          };
              
      },
    onSubmit () {
      
      this.loginState=true;
      this.showAlert=false;
      
      if (this.validateForm()) {
      
          let email = this.email.trim();
          let password = this.password;

          axios.post('/login', {
              email,
              password
          })

          .then(response => {
              if (response.data.isAuthenticated === "true") {
                  this.$router.push({ name: 'success'});
              } else {
                  
                  this.showAlert=true;
                  this.loginState=false;                  
                  this.errors.loginError=response.data.error;
              }
          })
          .catch(error => {
              console.log(error)
          })
      } else {

          this.showAlert=true;
          this.errors.loginError="Please complete all required fields to login."
          this.loginState=false;
      }
    },
  }
}
</script>

<style scoped>

</style>
