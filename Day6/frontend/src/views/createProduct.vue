<template>
    <div class="createProduct">
        <h1>This is an createProduct page</h1>
        <form>
            <input type="text" name="" id="" placeholder="name for product" v-model="this.name"><br><br>
            <input type="text" name="" id="" placeholder="dsec for product" v-model="this.desc"><br><br>
            <input type="number" name="" id="" placeholder="price for product" v-model="this.price"><br><br>
            <input type="number" name="" id="" placeholder="stock for product" v-model="this.stock"><br><br>
            <label for="cars">Choose a category:</label>
            <select name="cars" id="cars" v-model="this.id" v-if="categories">
                <option v-for="category in this.categories" :key="category.id"  :value=" category.id ">{{ category.name }}</option>
            </select><br><br>
            <label for="img">prod img: </label>
            <input type="file" name="img" id="omg" @change="addimg">
            <button type="button" @click="addProd">Create</button>
        </form>
        <p>{{ this.message }}</p>
        <!-- <p>{{ this.categories }}</p> -->
    </div>
</template>
<script>
import axios from 'axios';

export default{
    name: 'createProduct',
    data() {
        return {
            name: null,
            desc: null,
            token: null,
            message: null,
            price: null,
            stock: null,
            id: null,
            categories: null,
            img: null
        }
    },
    created(){
        this.token = localStorage.getItem('token')
        // console.log(this.token);
        if (!this.token){
            this.$router.push('/login');
        }else{
            this.fetchcategory()
        }
    },
    methods: {
        addimg(event){
            this.img = event.target.files[0]
            // console.log(this.img);
        },
        addProd(){
            let formdata = new FormData()
            formdata.append('name', this.name)
            formdata.append('description', this.desc)
            formdata.append('price', this.price)
            formdata.append('stock', this.stock)
            formdata.append('category_id', this.id)
            if(this.img){
                formdata.append('img', this.img)
            }else{
                alert('please select an image')
            }
            axios
            .post('http://localhost:5000/api/product',
            // {name: this.name, description: this.desc, price: this.price, stock: this.stock, category_id: this.id},
            formdata,
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
        },
        fetchcategory() {
            axios
            .get('http://localhost:5000/api/category',
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                // this.message = response.data.message
                if (response.status == 200){
                    this.categories = response.data.data
                }
            })
            .catch(error => {
                console.log(error);
                // this.message = error.response.data.message
            })
        }
    }
}
</script>