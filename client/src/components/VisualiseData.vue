<template>
  <div>
      <ForceGraph :data="data"></ForceGraph>
      <div style="padding-left: 50px; padding-top: 10px; text-align: center">
        <v-text-field v-model="inputUrl" label="Link do testowania"></v-text-field>
        <div class="my-2">
          <v-btn @click="changeData()" small color="primary">Get data</v-btn>
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
        data: null,
        inputUrl: "https://gist.githubusercontent.com/DawidPiechota/bc9eae88413e3546e7af2a92539f30bc/raw/7a2633381f014dd12feb810e56e6702ab30914a2/data3.json",
        dataList: ['data1.json', 'data2.json', 'data3.json'],
      }
    },
    mounted() {
      this.changeData();
    },
    methods: {
      changeData() {
    //     const dataIndex = Math.floor(Math.random() * this.dataList.length)
    //     d3.json("https://gist.githubusercontent.com/DawidPiechota/f4e95b3d5d4539c453003136d8f25db9/raw/1f3df31a88a19e20464f9c6b9b12f6ca17e9201d/data2.json",
    //     function(jsonData) {
    //     this.data = data;
    // });
        //wrapper for fetch basically
        d3.json(this.inputUrl)
        .then(data => {this.data = data})

        // d3.json(this.dataList[dataIndex]).then(data => {
        //   this.data = data
        // }).catch(error => {
        //   console.error('Cannot proceed with simulation, failed to  retrieve data.')
        // })
      }
    }
  }
</script>
