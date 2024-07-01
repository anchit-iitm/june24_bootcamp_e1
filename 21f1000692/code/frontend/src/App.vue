<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/login">login</router-link> |
    <router-link to="/register">register</router-link> |
    <router-link to="/createCategory">createCategory</router-link> |
    <router-link to="/createProduct">createProduct</router-link> |
    <router-link :to="{name: 'adminDash'}">Admin dashboard</router-link> |
    <a @click="logout_fn">logout</a> |
    <router-link to="/about">About</router-link>
  </nav>
  <!-- <p>from app.vue</p> -->
  <router-view/>
</template>


<script>
export default {
  methods: {
    logout_fn() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
