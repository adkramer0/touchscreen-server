<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 v-if="deviceState === Object(deviceState)" style="display: inline; float: inline-start;">{{ deviceState.name }}'s Settings</h5>
				<h5 v-else style="display: inline; float: inline-start;">Settings</h5>
				<div style="display: inline; float: inline-end;">
					<button @click="getDevice(id)" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-body">
				<div class="input-group mb-3">
					<input v-model="name" type="text" class="form-control" placeholder="New Device Name">
					<button :disabled="!name" @click="setDeviceName" class="btn btn-outline-info" type="button">Rename</button>
				</div>
				<div v-if="deviceState === Object(deviceState) && deviceState.online" class="btn-group btn-group-lg mb-3" role="group">
					<button @click="actionSetting('menu')" type="button" class="btn btn-outline-info">Menu Mode</button>
					<button @click="actionSetting('quit')" type="button" class="btn btn-outline-danger">Quit</button>
					<button @click="actionSetting('update')" type="button" class="btn btn-outline-warning">Update</button>
					<button @click="actionSetting('shutdown')" type="button" class="btn btn-outline-danger">Shutdown</button>
					<button @click="actionSetting('restart')" type="button" class="btn btn-outline-warning">Restart</button>
				</div>

			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'DeviceSettings',
		props: ['id'],
		data() {
			return {
				name: '',
			};
		},
		async created() {
			await this.getDevice(this.id);
		},
		computed: {
			...mapGetters({deviceState: 'stateDevice'}),
		},
		methods: {
			...mapActions(['getDevice', 'nameDevice', 'deviceSettings']),
			async setDeviceName() {
				await this.nameDevice({"id": this.id, "name": this.name});
				await this.getDevice(this.id);
			},
			async actionSetting(cmd) {
				let body = [{"id": this.id, "name": this.deviceState.name}];
				await this.deviceSettings({setting: cmd, devices: body });
				await this.getDevice(this.id);
			},
		},
	};
</script>