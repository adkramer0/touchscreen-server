<template>
  <div id="app">
    <NavBar/>
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';
  export default {
    components: {
      NavBar,
    },
  };
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #f1f7fc;
  color: #2c3e50;
  flex-grow:  1;
}
html {
  background-color: #f1f7fc;
}
</style>
