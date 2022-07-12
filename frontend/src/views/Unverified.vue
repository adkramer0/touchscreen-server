<template>
	<section>
		<div class="card border-info mb-3">
			<div class="card-header">
				<h5 style="display: inline; float: inline-start;">Unverified</h5>
				<div style="display: inline; float: inline-end;">
					<button @click="reload" class="btn btn-outline-info" type="button">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
							<path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
							<path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
						</svg>
					</button>
				</div>
			</div>
			<div class="card-body">
				{{ user.username }}, it looks like you're not verified yet. Have a current lab member verify you, then reload the page.
			</div>
		</div>
	</section>
</template>

<script>
	import {mapActions, mapGetters} from 'vuex';
	export default {
		name: 'Unverified',
		async created() {
			await this.reload();
		},
		computed: {
			...mapGetters({user: 'stateUser', isVerified: 'isVerified'}),
		},
		methods: {
			...mapActions(['whoAmI']),
			async reload() {
				await this.whoAmI()
				if (this.isVerified) {
					this.$router.push('/dashboard').catch(() => {});
				}
			}
		},
	};
</script>