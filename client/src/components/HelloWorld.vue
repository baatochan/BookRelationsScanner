<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
 <!--           <v-icon>mdi-home</v-icon>   -->
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Wczytaj tekst</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
 <!--           <v-icon>mdi-contact-mail</v-icon>   -->
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Zapisz graf</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Relacje pomiędzy bytami w tekstach literackich</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <VisualiseData/>
      <!-- <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col class="text-center">
            <v-tooltip left>
              <template v-slot:activator="{ on }">
                <v-btn
                  :href="source"
                  icon
                  large
                  target="_blank"
                  v-on="on"
                >
                  <v-icon large>mdi-code-tags</v-icon>
                </v-btn>
              </template>
              <span>Source</span>
            </v-tooltip>
          </v-col>
        </v-row>
      </v-container> -->
    </v-content>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
import VisualiseData from './VisualiseData.vue'

  export default {
    props: {
      source: String,
    },
    components: {
    VisualiseData
  },
    data: () => ({
      drawer: null,
    }),
  }
</script>
