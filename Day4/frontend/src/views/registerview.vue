<template>
    <div class="register">
        <h1>This is an register page</h1>
        <form>
            <label for="username">Email:</label><br>
            <input type="text" id="username" name="username" v-model="this.emailv"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" v-model="this.passwordv"><br>
            <label for="cars">Choose a role:</label>

            <select name="cars" id="cars" v-model="this.rolev">
                <option value="manager">manager</option>
                <option value="customer">customer</option>
            </select><br>
            <input type="button" @click="register_fn" value="signup">
        </form>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'RegisterView',
  data() {
    return {
      emailv: '',
      passwordv: '',
      rolev: ''
    }
  },
  methods: {
    register_fn() {
        axios
        .post('http://localhost:5000/api/register', {
            email: this.emailv,
            password: this.passwordv,
            role: this.rolev
        })
        .then(response => {
            console.log('catched response: '+ response.status)
            console.log(response.data.message);
            if (response.status == 201) {
                this.$router.push('/login');
            }
            
        })
        .catch(error => {
            console.log('catched error: ' + error)
        })
    }
  }
}
</script>