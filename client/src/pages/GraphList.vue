<template>
  <div style="background-color: white">
    <table>
      <tr>
        <th>Id</th>
        <th>Nazwa</th>
        <th>Status</th>
        <th>Wyświetl</th>
      </tr>
      <tr v-for="(item, index) in graphs" :key="index">
        <td class="text-center">{{ item[0] }}</td>
        <td class="text-center">{{ item[1] }}</td>
        <td class="text-center">{{ item[2] }}</td>
        <td class="text-center">
          <v-btn color="primary" :to="'/visualise-data/' + item[0]"
            >Przejdź</v-btn
          >
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      graphs: []
    };
  },
  created() {
    axios

      .get("http://127.0.0.1:5000/graphs", {
        headers: {
          "Content-type": "application/json"
        }
      })

      .then(response => {
        this.graphs = response.data.ghraps;
      })
      .catch(e => {
        this.errors.push(e);
      });
  }
};
</script>

<style scoped>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
