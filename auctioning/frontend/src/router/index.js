import { createWebHistory, createRouter } from "vue-router";
import homepage from '../views/homepage.vue'
import Profile from '../views/Profile.vue'
import Auction from '../views/Auction.vue'
import Upload from '../views/Upload.vue'


const routes = [
    {
        path: '/',
        name: 'homepage',
        component: homepage,
    },
    {
        path: '/Profile',
        name: 'Profile',
        component: Profile,
    },
    {
        path: '/Auction/:id',
        name: 'Auction',
        component: Auction,
    },
    {
        path: '/Upload',
        name: 'Upload',
        component: Upload,
    },





]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;