<template>
  <div id="app">
    <h1 class="logo-title">To Do List</h1>
    <ListManager></ListManager>
    <!-- <ToDoTable></ToDoTable> -->
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import ToDoTable from './components/ToDoTable.vue';
import ListManager from './components/ListManager.vue';
// import ToDoTable from './components/ToDoTable.vue';

export default {
  name: 'App',
  components: { ListManager }
}
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #390a2d;
  min-height: 100vh;
  margin: 0;
  background: linear-gradient(to right, #f43a3a, #7be4fe);
}

.logo-title {
  font-family: 'Arial', sans-serif;
  /* Use a font that suits your brand */
  color: #984caf;
  /* Choose a color that fits your site's theme */
  font-size: 32px;
  /* Adjust size as needed */
  text-shadow: 1px 1px 2px #000;
  /* Adds a shadow for a 3D effect */
  letter-spacing: 2px;
  /* Space out the letters slightly */
  text-transform: uppercase;
  /* Capitalize all letters for impact */
}</style>
