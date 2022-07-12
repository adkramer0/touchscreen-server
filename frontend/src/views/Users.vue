<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 style="display: inline; float: inline-start;">Manage Users</h5>
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
				<div v-if="Array.isArray(unverifiedUsersState) && unverifiedUsersState.length">
					<div class="btn-group mb-3" role="group">
						<button :disabled="!unverifiedUsers.length" @click="verify" type="button" class="btn btn-outline-info">Verify</button>
						<button :disabled="!unverifiedUsers.length" @click="deleteUnverified" type="button" class="btn btn-outline-danger">Delete</button>
					</div>
					<table class="table table-info table-bordered table-striped table-hover">
						<thead>
							<tr>
								<th>Username</th>
								<th>Select</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="user in unverifiedUsersState" :key="user.id">
								<td>{{ user.username }} </td>
								<td><input class="form-check-input" :value="{'id': user.id}" v-model= "unverifiedUsers" type="checkbox"></td>
							</tr>
						</tbody>
					</table>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Unverified Users
				</div>
			</div>

			<div class="card-body" v-else>
				<div v-if="Array.isArray(usersState) && usersState.length">
					<div class="mb-3">
						<button :disabled="!verifiedUsers.length" @click="deleteVerified" type="button" class="btn btn-outline-danger">Delete</button>
					</div>
					<table class="table table-info table-bordered table-striped table-hover">
						<thead>
							<tr>
								<th>Username</th>
								<th>Select</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="user in usersState" :key="user.id">
								<td>{{ user.username }}</td>
								<td v-if="currentUser.id !== user.id"><input class="form-check-input" :value="{'id': user.id}" v-model="verifiedUsers" type="checkbox"></td>
								<td v-else><input class="form-check-input" type="checkbox" disabled="disabled"></td>

							</tr>
						</tbody>
					</table>
				</div>
				<div class="alert alert-info" role="alert" v-else>
					No Verified Users
				</div>
			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'Users',
		data() {
			return {
				unverifiedUsers: [],
				verifiedUsers: [],
				isUnverifiedPage: true,
			};
		},
		async created() {
			await this.getUsers();
			await this.getUnverifiedUsers();
		},
		computed: {
			...mapGetters({usersState: 'stateUsers', unverifiedUsersState: 'stateUnverifiedUsers', currentUser: 'stateUser'}),
		},
		methods: {
			...mapActions(['verifyUsers', 'removeUsers', 'getUsers', 'getUnverifiedUsers']),
			async deleteUnverified() {
				await this.removeUsers(this.unverifiedUsers);
				this.unverifiedUsers = [];
				this.verifiedUsers = [];
			},
			async deleteVerified() {
				await this.removeUsers(this.verifiedUsers);
				this.verifiedUsers = [];
				this.unverifiedUsers = [];
			},
			async verify() {
				await this.verifyUsers(this.unverifiedUsers);
				this.unverifiedUsers = [];
				this.verifiedUsers = [];
			},
			async reload() {
				await this.getUsers();
				await this.getUnverifiedUsers();
				this.unverifiedUsers = [];
				this.verifiedUsers = [];
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