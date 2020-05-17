<template>
  <v-app id="app">
    <Menu v-bind:drawer="drawer" />
    <AppBar v-bind:change-drawer="changeDrawer" />
    <v-content>
      <v-container>
        <VisualiseData />
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
import VisualiseData from "../components/VisualiseData.vue";
import Menu from "../components/Layout/Menu";
import AppBar from "../components/Layout/AppBar";
import Footer from "../components/Layout/Footer";

export default {
  props: {
    source: String
  },
  components: {
    Footer,
    AppBar,
    Menu,
    VisualiseData
  },
  data: () => ({
    drawer: false
  }),
  methods: {
    changeDrawer() {
      this.drawer = !this.drawer;
    }
  }
};
</script>
