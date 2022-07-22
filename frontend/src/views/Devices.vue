<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 style="display: inline; float: inline-start;">Manage Devices</h5>
				<div style="display:  inline; float:	inline-end;">
					<button @click="reload" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-header">
				<ul class="nav nav-tabs card-header-tabs">
					<li class="nav-item">
						<a @click="setPage(true)" class="nav-link" :class="{ active: isUnverifiedPage }">Unverified</a>
					</li>
					<li class="nav-item">
						<a @click="setPage(false)" class="nav-link" :class="{ active: !isUnverifiedPage }">Verified</a>
					</li>
				</ul>
			</div>
			<div class="card-body" v-if="isUnverifiedPage">
				<div v-if="Array.isArray(unverifiedDevicesState) && unverifiedDevicesState.length">
					<div class="btn-group mb-3" role="group">
						<button :disabled="!unverifiedDevices.length" @click="verify" type="button" class="btn btn-outline-info">Verify</button>
						<button :disabled="!unverifiedDevices.length" @click="deleteUnverified" type="button" class="btn btn-outline-danger">Delete</button>
					</div>
					<table class="table table-info table-bordered table-striped table-hover">
						<thead>
							<tr>
								<th>Name</th>
								<th>Select</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="device in unverifiedDevicesState" :key="device.id">
								<td>{{ device.name }} </td>
								<td><input class="form-check-input" :value="{'id': device.id}" v-model="unverifiedDevices" type="checkbox"></td>
							</tr>
						</tbody>
					</table>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Unverified Devices
				</div>
			</div>

			<div class="card-body" v-else>
				<div v-if="Array.isArray(devicesState) && devicesState.length">
					<div class="mb-3">
						<button :disabled="!verifiedDevices.length" @click="deleteVerified" type="button" class="btn btn-outline-danger">Delete</button>
					</div>
					<table class="table table-info table-bordered table-striped table-hover">
						<thead>
							<tr>
								<th>Name</th>
								<th>Select</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="device in devicesState" :key="device.id">
								<td>{{ device.name }} </td>
								<td><input class="form-check-input" :value="{'id': device.id}" v-model="verifiedDevices" type="checkbox"></td>
							</tr>
						</tbody>
					</table>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Verified Devices
				</div>
			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'Devices',
		data() {
			return {
				unverifiedDevices: [],
				verifiedDevices: [],
				isUnverifiedPage: true,
			};
		},
		async created() {
			await this.getDevices();
			await this.getUnverifiedDevices();
			this.ws = new WebSocket('ws://localhost/api/users/stream');
			this.ws.onmessage = async (event) => {
				let data = JSON.parse(event.data);
				if (data.event === "update" && data.target == "devices") {
					await this.getDevices();
					await this.getUnverifiedDevices();
				}
			}
		},
		destroyed() {
			this.ws.close();
		},
		computed: {
			...mapGetters({devicesState: 'stateDevices', unverifiedDevicesState: 'stateUnverifiedDevices'}),
		},
		methods: {
			...mapActions(['verifyDevices', 'removeDevices', 'getDevices', 'getUnverifiedDevices']),
			async deleteUnverified() {
				await this.removeDevices(this.unverifiedDevices);
				this.unverifiedDevices = [];
				this.verifiedDevices = [];
			},
			async deleteVerified() {
				await this.removeDevices(this.verifiedDevices);
				this.verifiedDevices = [];
				this.unverifiedDevices = [];
			},
			async verify() {
				await this.verifyDevices(this.unverifiedDevices);
				this.unverifiedDevices = [];
				this.verifiedDevices = [];
			},
			async reload() {
				await this.getDevices();
				await this.getUnverifiedDevices();
				this.unverifiedDevices = [];
				this.verifiedDevices = [];
			},
			async setPage(unverified) {
				this.isUnverifiedPage = unverified;
				await this.reload();
			},
		},
	};
</script>
<style scoped>
	a {
		cursor: pointer;
	}
</style>