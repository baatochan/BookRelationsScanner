<template>
	<div id="load-file">
		<h1>Load text for analysis</h1>

		<form id="textinput-form">
			<p><label for="textinput-textarea">Paste here book text for analysis:</label></p>
			<textarea id="textinput-textarea" rows="10" v-model="text"></textarea>
			<p><label for="textinput-file">or upload a file below. Supported files: txt.</label></p>
			<label id="text-reader">
				Read File
				<input id="textinput-file" type="file" @change="loadTextFromFile">
			</label>

			<!--TODO: add button for sending form-->
		</form>
	</div>
</template>

<script>
export default{
	data: () => ({ text: "" }),
	methods: {
		loadTextFromFile(ev) {
			const file = ev.target.files[0];
			const reader = new FileReader();

			reader.onload = e => this.text = e.target.result;
			reader.readAsText(file);
		}
	}
}
</script>

<style>
#load-file {
	text-align: center;
	padding: 10px;
}

#load-file p {
	margin-bottom: 0;
}

#textinput-form {
	margin-top: 50px;
}

#textinput-textarea {
	width: 60%;
	height: 500px;
}

#text-reader {
	position: relative;
	overflow: hidden;
	display: inline-block;

	/* Fancy button style 😎 */
	border: 2px solid black;
	border-radius: 5px;
	padding: 8px 12px;
	cursor: pointer;
}
#text-reader input {
	position: absolute;
	top: 0;
	left: 0;
	z-index: -1;
	opacity: 0;
}
</style>
