<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld1 msg="Welcome to Your Vue.js App created by vue cli"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld1 from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld1
  }
}
</script>
