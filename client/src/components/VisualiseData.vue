<template>
  <div>
      <ForceGraph :data="data"></ForceGraph>
      <div style="padding-left: 50px; padding-top: 10px; text-align: center">
        <v-text-field v-model="inputUrl" label="Link do testowania"></v-text-field>
        <div class="my-2">
          <v-btn @click="changeData()" small color="primary">Get data</v-btn>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field v-model="nodeNameA" label="Byt (usuń)"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-text-field v-model="nodeNameB" label="Drugi byt (zachowaj)"></v-text-field>
            </v-col>
          </v-row>
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
        nodeNameA: null,
        nodeNameB: null,
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
        
        if (!this.exists(this.nodeNameA, this.nodeNameB)){
          alert("Byt o takiej nazwie nie istnieje!");
          return;
        } 
        var indexA = this.markNode(this.nodeNameA);
        var indexB = this.getIndexOfNode(this.nodeNameB)
        this.mergeLinks(indexA, indexB); //second one stays
        this.data = JSON.parse(JSON.stringify(this.changedData)); //update the data
      },
      mergeLinks(indexA, indexB){
        for (var i = 0; i < this.changedData.links.length; i++) { //B to target, B to mariusz Maciek-Mariusz
            var dupa = 0;
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
              this.changedData.links.splice(i, 1);
              break;
            default:
              // not possible
          }
        }
      },
      exists(nameA, nameB){
        var dupa = 0;
        for (var i = 0; i < this.changedData.nodes.length; i++)
          if (this.changedData.nodes[i].name == nameA || this.changedData.nodes[i].name == nameB)
            dupa++;
        if(dupa == 2) return true; else return false;
      },
      getIndexOfNode(name){
        for (var i = 0; i < this.changedData.nodes.length; i++)
          if (this.changedData.nodes[i].name == name)
            return i;
      },
      markNode(name) { //returns node index
        for (var i = 0; i < this.changedData.nodes.length; i++) {
          if (this.changedData.nodes[i].name == name) {
            this.changedData.nodes[i].name = "";
            return i; 
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
