<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 v-if="device === Object(device)" style="display: inline; float: inline-start;">{{ device.name }}'s Files</h5>
				<h5 v-else style="display: inline; float: inline-start;">Files</h5>
				<div style="display:  inline; float:	inline-end;">
					<button @click="getDevice(id)" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-body">
				<div  v-if="device === Object(device) && 'name' in device">
					<div v-if="Array.isArray(device.files) && device.files.length">
						<table class="table table-info table-bordered table-striped table-hover">
							<thead>
								<tr>
									<th>Name</th>
									<th>Download</th>
									<th><button :disabled="!files.length" @click="deleteFiles" type="button" class="btn btn-outline-danger">Delete</button></th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="file in device.files" :key="file.id">
									<td>{{ file.filename }}</td>
									<td>
										<a class="link-primary" @click="downloadDeviceFile(file.content_id)">
											<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-arrow-down-fill" viewBox="0 0 16 16">
												<path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zm-1 4v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 11.293V7.5a.5.5 0 0 1 1 0z"/>
											</svg>
										</a>
									</td>
									<td>
										<input class="form-check-input" :value="{'filename': file.filename, 'content_id': file.content_id, 'id': file.id, 'device_id': file.device_id}" v-model= "files" type="checkbox">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="alert alert-info" role="alert" v-else>
						{{ device.name }} has no files
					</div>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No device with id: {{ id }}
				</div>
			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'DeviceFiles',
		props: ['id'],
		data() {
			return {
				files: [],
			};
		},
		async created() {
			await this.getDevice(this.id);
		},
		computed: {
			...mapGetters({device: 'stateDevice'}),
		},
		methods: {
			...mapActions(['getDevice', 'removeDeviceFiles', 'downloadFile']),
			async deleteFiles() {
				await this.removeDeviceFiles(this.files);
				await this.getDevice(this.id);
				this.files = [];
			},
			async downloadDeviceFile(content_id) {
				await this.downloadFile(content_id);
				this.files = [];
			},
		},
	};
</script>

<style scoped>
	a {
		cursor: pointer;
	}
</style>