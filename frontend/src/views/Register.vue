<template>
	<section class="login-clean">
		<form @submit.prevent="submit">
			<div class="text-center">
				<h4 class="text-dark mb-4">Create an Account</h4>
			</div>
			<div class="mb-3 form-floating">
				<input v-model="user.username" type="text" class="form-control" name="username" placeholder="Username">
				<label for="username">Username</label>
			</div>
			<div class="mb-3 form-floating">
				<input v-model="user.email" type="email" class="form-control" name="email" placeholder="name@example.com">
				<label for="email">Email address</label>
			</div>
			<div class="mb-3 form-floating">
				<input v-model="user.password" type="password" class="form-control" name="password" placeholder="Password">
				<label for="password">Password</label>
			</div>
			<div class="mb-3">
				<button class="btn btn-primary d-block w-100" type="submit">Register</button>
			</div>
		</form>
	</section>
</template>

<script>
	import {mapActions} from 'vuex';
	export default {
		name: 'Register',
		data() {
			return {
				user: {
					username: '',
					email: '',
					password: '',
				},
			};
		},
		methods: {
			...mapActions(['register']),
			async submit() {
					await this.register(this.user);
					this.$router.push('/dashboard').catch(() => {});
			},
		},
	};
</script>

<style scoped>
.login-clean {
  background: #f1f7fc;
  padding: 80px 0;
}

.login-clean form {
  max-width: 320px;
  width: 90%;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 40px;
  border-radius: 4px;
  color: #505e6c;
  box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
}


.login-clean form .form-control {
  background: #f7f9fc;
  border: none;
  border-bottom: 1px solid #dfe7f1;
  border-radius: 0;
  box-shadow: none;
  outline: none;
  color: inherit;
  text-indent: 8px;
  height: 42px;
}

.login-clean form .btn-primary {
  background: #f4476b;
  border: none;
  border-radius: 4px;
  padding: 11px;
  box-shadow: none;
  margin-top: 26px;
  text-shadow: none;
  outline: none !important;
}

.login-clean form .btn-primary:hover, .login-clean form .btn-primary:active {
  background: #eb3b60;
}

.login-clean form .btn-primary:active {
  transform: translateY(1px);
}
</style>