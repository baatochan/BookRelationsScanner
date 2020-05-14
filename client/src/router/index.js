import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Instruction from '@/components/Instruction';
import LoadFile from '@/components/LoadFile';
import Graph from '@/components/Graph';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
	
	{
      path: '/instruction',
      name: 'Instruction',
      component: Instruction
    },
	
	{
      path: '/load-file',
      name: 'LoadFile',
      component: LoadFile
    },
	
	{
      path: '/graph',
      name: 'Graph',
      component: Graph
    },
  
  ]
});
