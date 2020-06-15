<template>
  <div style="background-color: white">
    <table>
      <tr>
        <th>Id</th>
        <th>Nazwa</th>
        <th>Status</th>
        <th>Wyświetl</th>
      </tr>
      <tr>
        <td>1</td>
        <td>test</td>
        <td>1</td>
        <td>przejdź</td>
      </tr>
      <tr>
        <td>2</td>
        <td>test2</td>
        <td>1</td>
        <td>przejdź</td>
      </tr>
      <tr>
        <td>3</td>
        <td>test3</td>
        <td>1</td>
        <td>przejdź</td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      graphs: [],
      errors: []
    };
  },

  methods: {
    log(message) {
      console.log(message);
    }
  },
  created() {
    axios

      .get("http://127.0.0.1:5000/graphs", {
        headers: {
          "Content-type": "application/json"
        }
      })

      .then(response => {
        this.graphs = response.data;
        console.log(JSON.phrase(response));
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
