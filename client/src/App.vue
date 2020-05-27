<template>
  <div id="app">
    <Layout />
  </div>
</template>

<script>
import Layout from "./pages/Layout";
export default {
  name: "App",
  components: {
    Layout
  }
};
</script>
<style scoped>
.RouterLink {
  text-decoration: none;
  color: #000000 !important;
}
.toolbar-title {
  text-decoration: none;
  color: #ffffff !important;
}
</style>
