import Vue from 'vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import axios from 'axios';

import App from './App.vue';

import store from './store';
import router from './router';


Vue.config.productionTip = false;

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost/api/'; //development



new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
