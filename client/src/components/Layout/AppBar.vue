<template>
  <v-app-bar app color="indigo" dark>
    <v-app-bar-nav-icon @click.stop="changeDrawer"></v-app-bar-nav-icon>
    <v-toolbar-title
      >Relacje pomiędzy bytami w tekstach literackich</v-toolbar-title
    >
  </v-app-bar>
</template>

<script>
export default {
  name: "AppBar",
  props: {
    changeDrawer: {
      type: Function,
      required: true
    }
  }
};
</script>

<style scoped></style>
