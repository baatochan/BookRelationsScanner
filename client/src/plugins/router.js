import Vue from "vue";
import Router from "vue-router";
import Home from "../pages/Home";
import LoadFile from "../pages/LoadFile";
import Instruction from "../pages/Instruction";
import VisualiseData from "../components/VisualiseData";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },

    {
      path: "/instruction",
      name: "Instruction",
      component: Instruction
    },

    {
      path: "/load-file",
      name: "LoadFile",
      component: LoadFile
    },

    {
      path: "/graph",
      name: "Graph",
      component: VisualiseData
    }
  ]
});
