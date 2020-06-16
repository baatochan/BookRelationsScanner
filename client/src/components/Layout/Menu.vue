<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list dense>
      <v-list-item link :to="`/visualise-data/0`">
        <v-list-item-content>
          <v-list-item-title class="text-center"
            >Visualise Data</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/force-graph">
        <v-list-item-content>
          <v-list-item-title class="text-center">Force Graph</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/load-file">
        <v-list-item-content>
          <v-list-item-title class="text-center">Load File</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/graph-list">
        <v-list-item-content>
          <v-list-item-title class="text-center"
            >Lista Grafów</v-list-item-title
          >
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
