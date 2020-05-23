<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list dense>
      <v-list-item link>
        <v-list-item-action> </v-list-item-action>
        <v-list-item-content>
          <router-link class="RouterLink" to="/visualise-data">
            <v-list-item-title>Visualise Data</v-list-item-title>
          </router-link>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link>
        <v-list-item-action> </v-list-item-action>
        <v-list-item-content>
          <router-link class="RouterLink" to="/force-graph">
            <v-list-item-title>Force Graph</v-list-item-title>
          </router-link>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link>
        <v-list-item-action> </v-list-item-action>
        <v-list-item-content>
          <router-link class="RouterLink" to="/load-file">
            <v-list-item-title>Load File</v-list-item-title>
          </router-link>
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
