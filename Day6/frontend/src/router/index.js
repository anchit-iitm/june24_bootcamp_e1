import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/registerview.vue'
import createProduct from '@/views/createProduct.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/loginview.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/createcategory',
    name: 'createCategory',
    component: () => import('@/views/createCategory.vue')
  },
  {
    path: '/updateCategory/:id',
    name: 'updateCategory',
    component: () => import('@/views/updateCategory.vue')
  },
  {
    path: '/createProduct',
    name: 'createProduct',
    component: createProduct
  },
  {
    path: '/admindash',
    name: 'adminDash',
    component: () => import('@/views/adminDash.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
