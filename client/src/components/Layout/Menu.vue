<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list dense>
      <v-list-item link>
        <v-list-item-action> </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Wczytaj tekst</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link>
        <v-list-item-action> </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Zapisz graf</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Menu",
  props: {
    drawer: {
      type: Boolean,
      required: true
    }
  }
};
</script>

<style scoped></style>
