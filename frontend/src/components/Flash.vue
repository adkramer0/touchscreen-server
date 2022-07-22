<template>
	<div class="alert alert-danger alert-dismissible" role="alert">
		<strong>Error {{ status_code }}:</strong> {{ message }}
		<button @click="dismissFlash(index)" type="button" class="btn-close"></button>
	</div>
</template>
<script>
	import {mapActions} from 'vuex';
	export default {
		name: 'Flash',
		props: ['message', 'status_code', 'index'],
		methods: {
			...mapActions(['dismissFlash']),
		},

	};
</script>