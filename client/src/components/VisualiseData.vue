<template>
  <v-row justify="center" align="center">
    <v-row>
      <ForceGraph :data="data"></ForceGraph>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="inputUrl"
              label="Link do testowania"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn @click="changeData()" small color="primary">Get data</v-btn>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="6">
            <v-autocomplete
              v-model="nodeNameA"
              :items="items"
              dense
              filled
              label="Byt (usuń)"
            ></v-autocomplete>
          </v-col>
          <v-col cols="6">
            <v-autocomplete
              v-model="nodeNameB"
              :items="items"
              dense
              filled
              label="Drugi byt (zachowaj)"
            ></v-autocomplete>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn @click="mergeNodes()" small color="primary">Merge</v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-row>
</template>

<script>
import ForceGraph from "./ForceGraph.vue";
import * as d3 from "d3";

export default {
  components: {
    ForceGraph
  },
  data() {
    return {
      nodeNameA: null,
      nodeNameB: null,
      items: null,
      originalData: null,
      data: null,
      changedData: null,
      inputUrl:
        "https://gist.githubusercontent.com/DawidPiechota/bc9eae88413e3546e7af2a92539f30bc/raw/7a2633381f014dd12feb810e56e6702ab30914a2/data3.json",
      dataList: ["data1.json", "data2.json", "data3.json"]
    };
  },
  mounted() {
    this.changeData();
  },
  methods: {
    nodes() {
      this.items = this.changedData.nodes
        .filter(d => {
          if (d.name === "") {
            return false;
          }
          return true;
        })
        .map(d => d.name);
      return this.items;
    },
    mergeNodes() {
      if (!this.exists(this.nodeNameA, this.nodeNameB)) {
        alert("Coś nie tak");
        return;
      }
      const indexA = this.markNode(this.nodeNameA);
      const indexB = this.getIndexOfNode(this.nodeNameB);
      this.mergeLinks(indexA, indexB); // second one stays
      this.data = JSON.parse(JSON.stringify(this.changedData)); // update the data
      this.items = this.nodes();
      this.nodeNameA = "";
      this.nodeNameB = "";
    },
    mergeLinks(indexA, indexB) {
      for (let i = 0; i < this.changedData.links.length; i++) {
        let dupa = 0;
        if (this.changedData.links[i].source === indexA) {
          dupa += 1;
        }
        if (this.changedData.links[i].target === indexA) {
          dupa += 2;
        }

        switch (dupa) {
          case 1:
            this.changedData.links[i].source = indexB;
            break;
          case 2:
            this.changedData.links[i].target = indexB;
            break;
          case 3:
            // this.changedData.links.splice(i, 1); dalej powoduje błędy. Na razie zostawię tak, powinno działać bez tego
            break;
          default:
          // not possible
        }
      }
    },
    exists(nameA, nameB) {
      let dupa = 0;
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (
          this.changedData.nodes[i].name === nameA ||
          this.changedData.nodes[i].name === nameB
        ) {
          dupa++;
        }
      }
      if (dupa === 2) return true;
      else return false;
    },
    getIndexOfNode(name) {
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (this.changedData.nodes[i].name === name) {
          return i;
        }
      }
    },
    markNode(name) {
      // returns node index
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (this.changedData.nodes[i].name === name) {
          this.changedData.nodes[i].name = "";
          return i;
        }
      }
    },
    changeData() {
      // wrapper for fetch basically
      d3.json(this.inputUrl).then(data => {
        this.originalData = data;
        this.changedData = JSON.parse(JSON.stringify(data)); // Hacky way to copy json
        this.data = JSON.parse(JSON.stringify(data));
        this.items = this.nodes();
      });
    }
  }
};
</script>
