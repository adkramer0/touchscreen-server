import createPersistedState from "vuex-persistedstate";
import Vue from 'vue';
import Vuex from 'vuex';

import users from './modules/users';
import devices from './modules/devices';
import flashes from './modules/flashes';

Vue.use(Vuex);
// create Vuex Store to persist state on page reload
export default new Vuex.Store({
	modules: {
		users,
		devices,
		flashes,
	},
	plugins: [createPersistedState()]
});