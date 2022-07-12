import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store';
import Dashboard from '@/views/Dashboard.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import Devices from '@/views/Devices.vue';
import Users from '@/views/Users.vue';
import DeviceFiles from '@/views/DeviceFiles.vue';
import DeviceSettings from '@/views/DeviceSettings.vue';
import Protocols from '@/views/Protocols.vue';
import Unverified from '@/views/Unverified.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    alias: '/dashboard',
    name: 'Dashboard',
    meta: {requiresAuth: true, title: 'Dashboard | Touchscreen'},
    component: Dashboard,
  },
  {
    path: '/register',
    name: 'Register',
    meta: {title: 'Register | Touchscreen'},
    component: Register,
  },
  {
    path: '/login',
    name: 'Login',
    meta: {title: 'Login | Touchscreen'},
    component: Login,
  },
  {
    path: '/unverified',
    name: 'Unverified',
    meta: {title: 'Unverified | Touchscreen'},
    component: Unverified
  },
  {
    path: '/devices',
    name: 'Devices',
    meta: {requiresAuth: true, title: 'Devices | Touchscreen'},
    component: Devices,
  },
  {
    path: '/users',
    name: 'Users',
    meta: {requiresAuth: true, title: 'Users | Touchscreen'},
    component: Users,
  },
  {
    path: '/protocols',
    name: 'Protocols',
    meta: {requiresAuth: true, title: 'Protocols | Touchscreen'},
    component: Protocols,
  },
  {
    path: '/devices/:id/files',
    name: 'DeviceFiles',
    meta: {requiresAuth: true, title: 'Files | Touchscreen'},
    component: DeviceFiles,
    props: true,
  },
  {
    path: '/devices/:id/settings',
    name: 'DeviceSettings',
    meta: {requiresAuth: true, title: 'Settings | Touchscreen'},
    component: DeviceSettings,
    props: true,
  },

];


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Touchscreen';
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters['isAuthenticated']) {
      if (store.getters['isVerified']) {
        next();
      }
      else {
        document.title = 'Unverified | Touchscreen';
        next('/unverified');
      }
    }
    else {
      document.title = 'Login | Touchscreen';
      next('/login');
    }
  } else {
    next();
  }
});



export default router;
