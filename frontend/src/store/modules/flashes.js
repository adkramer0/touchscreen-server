const state = {
	flashes: [],
};


const getters = {
	flashes: state => state.flashes,
};

const actions = {
	dismissFlash({commit}, index) {
		commit('remove', index);
	},
	flash({commit}, response) {
		commit('add', response);
	},
	clearFlashes({commit}) {
		commit('removeAll');
	}
};

const mutations = {
	add(state, response) {
		if (Array.isArray(response.data.detail)) {
			response.data.detail.forEach(item => state.flashes.unshift({status_code: response.status, message: item.msg}));
		} else {
			state.flashes.unshift({status_code: response.status, message: response.data.detail});
		}
		
	},
	remove(state, index) {
		state.flashes.splice(index, 1);
	},
	removeAll(state) {
		state.flashes = [];
	}
};

export default {
	state,
	getters,
	actions,
	mutations
};