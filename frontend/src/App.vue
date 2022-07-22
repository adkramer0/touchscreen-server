<template>
  <div id="app">
    <NavBar/>
    <div class="container">
      <Flash v-for="(flash, index) in flashes" v-bind:status_code="flash.status_code" v-bind:message="flash.message" v-bind:index="index" v-bind:key="index"/>
      <router-view/>
    </div>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue';
  import Flash from '@/components/Flash.vue';
  import {mapGetters} from 'vuex';
  export default {
    components: {
      NavBar,
      Flash,
    },
    computed: {
      ...mapGetters({flashes: 'flashes'}),
    }
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
