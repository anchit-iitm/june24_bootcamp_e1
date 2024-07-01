<template>
    <div class="createCategory">
      <h1>This is an createCategory page</h1>
      <form>
        <input type="text" name="" id="" placeholder="name for category" v-model="this.name"><br><br>
        <input type="text" name="" id="" placeholder="dsec for category" v-model="this.desc"><br><br>
        <button type="button" @click="addCategory">Create</button>
      </form>
      <p>{{ this.message }}</p>
    </div>
</template>
<script>
import axios from 'axios';

export default{
    name: 'createCategory',
    data() {
        return {
            name: null,
            desc: null,
            token: null,
            message: null
        }
    },
    created(){
        this.token = localStorage.getItem('token')
        // console.log(this.token);
        if (!this.token){
            this.$router.push('/login');
        }
    },
    methods: {
        addCategory(){
            axios
            .post('http://localhost:5000/api/category',
            {name: this.name, description: this.desc},
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                this.message = response.data.message
                if (response.status == 201){
                    this.$router.push('/')
                }
            })
            .catch(error => {
                console.log(error);
                this.message = error.response.data.message
            })
        }
    }
}
</script>