<template>
	<div class="app" >
	
		<mdb-navbar color="indigo" dark >
		<mdb-navbar-brand href="https://mdbootstrap.com/">
			Relacje pomiędzy bytami w tekstach literackich
		</mdb-navbar-brand>
		<mdb-navbar-toggler>
		<mdb-navbar-nav>
			<mdb-nav-item href="/">Home</mdb-nav-item>
			<mdb-nav-item href="#/instruction">Instruction</mdb-nav-item>
			<mdb-nav-item href="#/load-file">load-file</mdb-nav-item>
			<mdb-nav-item href="#/graph">Graph</mdb-nav-item> 
		</mdb-navbar-nav>
		</mdb-navbar-toggler>
		</mdb-navbar>

			<v-content>
				<router-view/>
			</v-content>






	</div>
  </template>







<script>
  import { mdbNavbar, mdbNavbarBrand, mdbNavbarToggler, mdbNavbarNav, mdbNavItem } from 'mdbvue';
  export default {
    name: 'NavbarPage',
    components: {
      mdbNavbar,
      mdbNavbarBrand,
      mdbNavbarToggler,
      mdbNavbarNav,
      mdbNavItem,
	
    }
  }
</script>













<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
