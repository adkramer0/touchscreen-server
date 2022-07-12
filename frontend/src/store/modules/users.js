import axios from 'axios';

const state = {
	user: null,
	users: null,
	unverifiedUsers: null,
	protocols: null,
};

const getters = {
	isAuthenticated: state => !!state.user,
	isVerified: state => !!state.user.verified,
	stateUser: state => state.user,
	stateUsers: state => state.users,
	stateUnverifiedUsers: state => state.unverifiedUsers,
	stateProtocols: state => state.protocols,
};

const actions = {
	async register({dispatch}, form) {
		await axios.post('users/register', form);
		let LoginForm = new FormData();
		LoginForm.append('username', form.username);
		LoginForm.append('password', form.password);
		LoginForm.append('scope', 'user')
		await dispatch('logIn', LoginForm);
	},
	async logIn({dispatch}, user) {
		await axios.post('token', user);
		await dispatch('whoAmI');
	},
	async whoAmI({commit}) {
		let {data} = await axios.get('users/whoami');
		commit('setUser', data);
	},
	async getUsers({commit}) {
		let {data} = await axios.get('users/?verified=true');
		commit('setUsers', data);
	},
	async getUnverifiedUsers({commit}) {
		let {data} = await axios.get('users/?verified=false');
		commit('setUnverifiedUsers', data);		
	},
	async verifyUsers({dispatch}, users) {
		await axios.put('users/verify', users);
		await dispatch('getUnverifiedUsers');
		await dispatch('getUsers');
	},
	async removeUsers({dispatch}, users) {
		await axios.delete('users/remove', {data: users});
		await dispatch('getUnverifiedUsers');
		await dispatch('getUsers');
	},
	async getProtocols({commit}) {
		let {data} = await axios.get('users/protocols');
		commit('setProtocols', data);
	},
	async removeProtocols({dispatch}, protocols) {
		await axios.delete('users/remove/protocols', {data: protocols});
		await dispatch('getProtocols');
	},
	async uploadProtocols({dispatch}, protocolFiles) {
		let formData = new FormData();
		for (let i = 0; i < protocolFiles.length; i++) {
			formData.append('files', protocolFiles[i]);
		}
		await axios.post('users/upload', formData, {headers: {"Content-Type": "multipart/form-data",},});
		await dispatch('getProtocols');
	},
	// eslint-disable-next-line no-empty-pattern
	async downloadFile({}, file) {
		window.open(axios.defaults.baseURL + `users/download/${file}`);
	},
	resetUserState({commit}) {
		commit('resetUser');
	},
	// eslint-disable-next-line no-empty-pattern
	async deleteCookie({}) {
		await axios.get('token/remove');
	}
};

const mutations = {
	setUser(state, user) {
		state.user = user;
	},
	setUsers(state, users) {
		state.users = users;
	},
	setUnverifiedUsers(state, unverifiedUsers) {
		state.unverifiedUsers = unverifiedUsers;
	},
	setProtocols(state, protocols) {
		state.protocols = protocols;
	},
	resetUser(state) {
		state.user = null;
		state.users = null;
		state.unverifiedUsers = null;
		state.protocols = null;
	},
};

export default {
	state,
	getters,
	actions,
	mutations
};