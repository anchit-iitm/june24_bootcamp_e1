<template>
    <div>
    <h1>update category: {{ this.name1 }}</h1>
    <form>
        <input type="text" name="" id="" placeholder="name for category" v-model="this.name"><br><br>
        <input type="text" name="" id="" placeholder="dsec for category" v-model="this.desc"><br><br>
        <button type="button" @click="upCategory">Update</button>
    </form>
    <p>{{ this.message }} </p>
    </div>
</template>
<script>
import axios from 'axios';
export default{
    data() {
        return {
            token: null,
            message: null,
            category_id: null,
            name: null,
            name1: null,
            desc: null
        }
    },
    created(){
        this.category_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        // console.log(this.token);
        if (!this.token){
            this.$router.push('/login');
        }else{
            this.fetchcategory()
        }
    },
    methods: {
        fetchcategory() {
            axios
            .get(`http://localhost:5000/api/category/${this.category_id}`,
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                // this.message = response.data.message
                if (response.status == 200){
                    // this.categories = response.data.data
                    this.name = response.data.data.name
                    this.name1 = response.data.data.name
                    this.desc = response.data.data.description
                    this.message = response.data.message
                }
            })
            .catch(error => {
                console.log(error);
                // this.message = error.response.data.message
            })
        },
        upCategory(){
            axios
            .put(`http://localhost:5000/api/category/${this.category_id}`,
            {name: this.name, description: this.desc},
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                this.message = response.data.message
                if (response.status == 201){
                    this.$router.push('/admindash')
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