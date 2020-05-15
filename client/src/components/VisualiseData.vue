<template>
  <div>
      <ForceGraph :data="data"></ForceGraph>
      <div style="padding-left: 50px; padding-top: 10px; text-align: center">
        <v-text-field v-model="inputUrl" label="Link do testowania"></v-text-field>
        <div class="my-2">
          <v-btn @click="changeData()" small color="primary">Get data</v-btn>
          <v-btn @click="mergeNodes()" small color="primary">Merge</v-btn>
        </div>
      </div>
    </div>
</template>


<script>
import ForceGraph from './ForceGraph.vue'
import * as d3 from "d3";

export default {
    components: {
      ForceGraph
    },
    data() {
      return {
        originalData: null,
        data: null,
        changedData: null,
        inputUrl: "https://gist.githubusercontent.com/DawidPiechota/bc9eae88413e3546e7af2a92539f30bc/raw/7a2633381f014dd12feb810e56e6702ab30914a2/data3.json",
        dataList: ['data1.json', 'data2.json', 'data3.json'],
      }
    },
    mounted() {
      this.changeData();
      //this.changedData = JSON.parse(JSON.stringify(this.originalData)); //Hacky way to copy json
      //this.data = JSON.parse(JSON.stringify(this.originalData));
    },
    methods: {
      mergeNodes(){
        this.markNode("Mariusz");
        this.mergeLinks(12, 0); //second one stays
        this.data = JSON.parse(JSON.stringify(this.changedData)); //update the data
      },
      mergeLinks(indexA, indexB){
        var dupa = 0;
        for (var i = 0; i < this.changedData.links.length; i++) {
            if (this.changedData.links[i].source == indexA)
              dupa += 1;
            if (this.changedData.links[i].target == indexA)
              dupa += 2;

            switch(dupa) {
            case 1:
              this.changedData.links[i].source = indexB
              break;
            case 2:
              this.changedData.links[i].target = indexB
              break;
            case 3:
              delete this.changedData.links[i]
              break;
            default:
              // not possible (i think)
          }
        }
      },
      markNode(name) {
        for (var i = 0; i < this.changedData.nodes.length; i++) {
          if (this.changedData.nodes[i].name == name) {
            this.changedData.nodes[i].name = "dupa123";
            return i; //returns node index
          }
        }
      },
      changeData() {
        //wrapper for fetch basically
        d3.json(this.inputUrl)
        .then(data => {
          this.originalData = data
          this.changedData = JSON.parse(JSON.stringify(data)); //Hacky way to copy json
          this.data = JSON.parse(JSON.stringify(data));
          })
      }
    }
  }
</script>
