<template>
    <div class="adminDash">
        <h1>This is an admin dashboard page</h1>
        <input type="text" placeholder="search" v-model="search">
        
        <div v-if="!search">
            <h2>categories</h2>
            <table>
                <thead>
                    <tr>
                        <th>name</th>
                        <th>desc</th>
                        <th>status | delete</th>
                        <th>action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in categories" :key="category.id">
                        <td>{{ category.name }}</td>
                        <td>{{ category.description }}</td>
                        <td>{{ category.status }} | {{ category.delete }}</td>
                        <td>
                            <router-link :to="{ name: 'updateCategory', params: { id: category.id } }">update</router-link> 
                            | 
                            <a v-if="!category.delete" @click="deleteCategory(category.id)">delete</a>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <h2>products</h2>
            <table>
                <thead>
                    <tr>
                        <th>name</th>
                        <th>desc</th>
                        <th>status | delete</th>
                        <th>action</th>
                        <th>image</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in products" :key="product.id">
                        <td>{{ product.name }}</td>
                        <td>{{ product.description }}</td>
                        <td>{{ product.status }} | {{ product.delete }}</td>
                        <td>
                            <router-link :to="{ name: 'updateCategory', params: { id: product.id } }">update</router-link> 
                            | 
                            <button v-if="!product.delete" @click="deleteProduct(product.id)">delete</button>
                        </td>
                        <td><img :src="`http://localhost:8000/${product.id}.jpg`" alt="" height="20" width="20"></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div v-else>
            <h2>category</h2>
            <p v-if="filteredCategories.length === 0">No category found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>name</th>
                        <th>desc</th>
                        <th>status | delete</th>
                        <th>action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in filteredCategories" :key="category.id">
                        <td>{{ category.name }}</td>
                        <td>{{ category.description }}</td>
                        <td>{{ category.status }} | {{ category.delete }}</td>
                        <td>
                            <router-link :to="{ name: 'updateCategory', params: { id: category.id } }">update</router-link> 
                            | 
                            <a v-if="!category.delete" @click="deleteCategory(category.id)">delete</a>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <h2>products</h2>
            <p v-if="filteredProducts.length === 0">No products found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>name</th>
                        <th>desc</th>
                        <th>status | delete</th>
                        <th>action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in filteredProducts" :key="product.id">
                        <td>{{ product.name }}</td>
                        <td>{{ product.description }}</td>
                        <td>{{ product.status }} | {{ product.delete }}</td>
                        <td>
                            <router-link :to="{ name: 'updateCategory', params: { id: product.id } }">update</router-link> 
                            | 
                            <button v-if="!product.delete" @click="deleteProduct(product.id)">delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            token: null,
            message: null,
            categories: [],
            products: [],
            search: ''
        }
    },
    computed: {
        filteredCategories() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.categories.filter(category => category.name.toLowerCase().includes(searchLower));
        },
        filteredProducts() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.products.filter(product => product.name.toLowerCase().includes(searchLower));
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        if (!this.token) {
            this.$router.push('/login');
        } else {
            this.fetchcategory();
            this.fetchprod();
        }
    },
    methods: {
        fetchcategory() {
            axios
                .get('http://localhost:5000/api/category', {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 200) {
                        this.categories = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        fetchprod() {
            axios
                .get('http://localhost:5000/api/product', {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 200) {
                        this.products = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteCategory(id) {
            axios
                .delete(`http://localhost:5000/api/category/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 201) {
                        this.fetchcategory();
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteProduct(id) {
            axios
                .delete(`http://localhost:5000/api/product/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 201) {
                        this.fetchprod();
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>
