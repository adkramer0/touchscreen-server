<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 style="display: inline; float: inline-start;">Manage Protocols</h5>
				<div style="display:  inline; float:	inline-end;">
					<button @click="getProtocols" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-body">
				<div class="input-group mb-3">
					<input v-if="ready" @change="selectFiles" type="file" multiple class="form-control">
					<button :disabled="!selectedFiles.length" @click="uploadProtocolFiles" class="btn btn-outline-info" type="button" >Upload Protocols</button>
				</div>
				<div v-if="Array.isArray(files) && files.length" class="input-group mb-3">
					<label class="input-group-text" for="inputGroupFiles">Protocol Files</label>
					<select v-model="selectedFile" class="form-select" id="inputGroupFiles">
						<option v-for="file in files" :key="file.id" :value="file">{{ file.filename }}</option>
					</select>
					<button :disabled="selectedFile === Object(selectedFile) && !('id' in selectedFile)" @click="downloadProtocol" class="btn btn-outline-info" type="button">Download</button>
					<button :disabled="selectedFile === Object(selectedFile) && !('id' in selectedFile)" @click="deleteFile" class="btn btn-outline-danger" type="button">Delete</button>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Files
				</div>
				<div v-if="selectedFile === Object(selectedFile) && 'protocols' in selectedFile" class="input-group mb-3">
					<label class="input-group-text" for="inputGroupProtocols">Protocols</label>
					<select v-model="selectedProtocol" class="form-select" id="inputGroupProtocols">
						<option v-for="protocol in selectedFile.protocols" :key="protocol" :value="protocol">{{ protocol }}</option>
					</select>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Protocols
				</div>
			</div>
		</div>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 style="display: inline; float: inline-start;">Online Devices</h5>
				<div style="display:  inline; float:	inline-end;">
					<button @click="getActiveDevices" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-body">
				<div class="mb-3" v-if="Array.isArray(activeDevices) && activeDevices.length">
					<div class="btn-group mb-3" role="group" aria-label="Basic mixed styles example">
						<button :disabled="!selectedDevices.length" v-if="selectedProtocol" @click="runProtocol" class="btn btn-outline-info" type="button">Run {{ selectedProtocol }}</button>
						<button :disabled="!selectedDevices.length" @click="stopProtocol" type="button" class="btn btn-outline-danger">End Active Protocols</button>
					</div>
					<table class="table table-info table-bordered table-striped table-hover">
						<thead>
							<tr>
								<th>Name</th>
								<th>Select</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="device in activeDevices" :key="device.id">
								<td>{{ device.name }}</td>
								<td><input class="form-check-input" :value="device" v-model="selectedDevices" type="checkbox"></td>
							</tr>
						</tbody>
					</table>
				</div>
				<div class="alert alert-info mb-3" role="alert" v-else>
					No Active Devices
				</div>
			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'Protocols',
		data() {
			return {
				selectedFile: {},
				selectedProtocol: '',
				selectedDevices: [],
				selectedFiles: [],
				ready: true,
			};
		},
		async created() {
			await this.getProtocols();
			await this.getActiveDevices();
		},
		computed: {
			...mapGetters({files: 'stateProtocols', activeDevices: 'stateActiveDevices'}),
		},
		methods: {
			...mapActions(['getActiveDevices', 'runDevices', 'stopDevices', 'getProtocols', 'removeProtocols', 'uploadProtocols', 'downloadFile']),
			async deleteFile() {
				await this.removeProtocols([this.selectedFile]);
				this.selectedFile = {};
				this.selectedProtocol = '';
			},
			async downloadProtocol() {
				await this.downloadFile(this.selectedFile.content_id);
			},
			async runProtocol() {
				let request = {'id': this.selectedFile.id, 'filename': this.selectedFile.filename, 'protocol': this.selectedProtocol, 'devices': this.selectedDevices};
				await this.runDevices(request);
			},
			async stopProtocol() {
				await this.stopDevices(this.selectedDevices);
				this.selectedDevices = [];
			},
			async uploadProtocolFiles() {
				await this.uploadProtocols(this.selectedFiles);
				// reset file input (can't use v-model because read only)
				this.ready = false;
				this.$nextTick(() =>{
					this.ready = true;
				});
				this.selectedFiles = [];
			},
			selectFiles() {
				this.selectedFiles = event.target.files;
			},
		},
	};
</script>