import axios from 'axios';

const state = {
	devices: null,
	device: null,
	unverifiedDevices: null,
	activeDevices: null,
};

const getters = {
	stateDevices: state => state.devices,
	stateDevice: state => state.device,
	stateUnverifiedDevices: state => state.unverifiedDevices,
	stateActiveDevices: state => state.activeDevices,
};

const actions = {
	async getDevices({commit}) {
		let {data} = await axios.get('users/devices?verified=true');
		commit('setDevices', data);
	},
	async getUnverifiedDevices({commit}) {
		let {data} = await axios.get('users/devices?verified=false');
		commit('setUnverifiedDevices', data);
	},
	async getDevice({commit}, device) {
		let {data} = await axios.get(`users/devices/${device}`);
		commit('setDevice', data);
	},
	async getActiveDevices({commit}) {
		let {data} = await axios.get('users/devices/active');
		commit('setActiveDevices', data);
	},
	async verifyDevices({dispatch}, devices) {
		await axios.put('users/verify/devices', devices);
		await dispatch('getUnverifiedDevices');
		await dispatch('getDevices');
	},
	async nameDevice({dispatch}, device) {
		await axios.put('users/name/device', device);
		await dispatch('getDevices');
	},
	async removeDevices({dispatch}, devices) {
		await axios.delete('users/remove/devices', {data: devices});
		await dispatch('getDevices');
		await dispatch('getUnverifiedDevices');
	},
	async runDevices({dispatch}, protocolDevices) {
		await axios.post('users/devices/run', protocolDevices);
		await dispatch('getActiveDevices');
	},
	async stopDevices({dispatch}, devices) {
		await axios.post('users/devices/stop', devices);
		await dispatch('getActiveDevices');
	},
	// eslint-disable-next-line no-empty-pattern
	async removeDeviceFiles({}, files) {
		await axios.delete('users/remove/files', {data: files});
	},
	async deviceSettings({dispatch}, { setting, devices }) {
		await axios.post(`users/devices/settings/${setting}`, devices);
		await dispatch('getActiveDevices');
	},
	resetDeviceState({commit}) {
		commit('resetDevices');
	},

};

const mutations = {
	setDevices(state, devices) {
		state.devices = devices;
	},
	setUnverifiedDevices(state, unverifiedDevices) {
		state.unverifiedDevices = unverifiedDevices;
	},
	setActiveDevices(state, activeDevices) {
		state.activeDevices = activeDevices;
	},
	setDevice(state, device) {
		state.device = device;
	},
	resetDevices(state) {
		state.devices = null;
		state.device = null;
		state.unverifiedDevices = null;
		state.activeDevices = null;
	}
};

export default {
	state,
	getters,
	actions,
	mutations
};