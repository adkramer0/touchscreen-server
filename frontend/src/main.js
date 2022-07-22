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

axios.interceptors.response.use(undefined, function(error) {
  if (error) {
    if (error.response.status === 401 && !error.config._retry && !(error.config.url === 'token' || error.config.url === 'users/register')) {
      error.config._retry = true;
      store.dispatch('resetDeviceState');
      store.dispatch('resetUserState');
      store.dispatch('deleteCookie');
      router.push('/login');
      return Promise.reject(error);

    } else {
      store.dispatch('flash', error.response);
      return Promise.reject(error);
    }
  }
});

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
