<template>
	<header class="mb-3">
		<nav class="navbar navbar-expand-md navbar-dark bg-secondary sticky-top">
			<div class="container-fluid d-flex">
				<router-link class="navbar-brand" to="/dashboard">Touchscreen</router-link>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarToggler">
					<ul v-if="isAuthenticated" class="navbar-nav me-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<router-link class="nav-link" to="/dashboard">Dashboard</router-link>
						</li>
						<li v-show="isVerified" class="nav-item">
							<router-link class="nav-link" to="/devices">Devices</router-link>
						</li>
						<li v-show="isVerified" class="nav-item">
							<router-link class="nav-link" to="/users">Users</router-link>
						</li>

						<li v-show="isVerified" class="nav-item">
							<router-link class="nav-link" to='/protocols'>Protocols</router-link>
						</li>
					</ul>
					<ul v-else class="navbar-nav ms-md-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<router-link class="nav-link" to="/login">Log In</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/register">Register</router-link>
						</li>
					</ul>
					<ul v-if="isAuthenticated" class="navbar-nav ms-md-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<a class="nav-link" @click="logOut">Log Out</a>
						</li>
					</ul>

				</div>
			</div>
		</nav>
	</header>
</template>

<script>
	import {mapGetters} from 'vuex';
	export default {
		name: 'NavBar',
		computed: {
			...mapGetters({isAuthenticated: 'isAuthenticated', isVerified: 'isVerified'}),
		},
		methods: {
			async logOut () {
				this.$store.dispatch('resetDeviceState');
				this.$store.dispatch('resetUserState');
				this.$store.dispatch('deleteCookie');
				this.$router.push('/login');
			},

		}
	};
</script>

<style scoped>
	a {
		cursor: pointer;
	}
</style>