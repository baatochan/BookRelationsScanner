<template>
  <div id="load-file">
    <loading
      :active.sync="isLoading"
      :can-cancel="false"
      :on-cancel="onCancel"
      :is-full-page="fullPage"
    ></loading>
    <v-row justify="center" align="center">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col cols="12" align="center">
              <h1>Load text for analysis</h1>
            </v-col>
          </v-row>
          <v-row v-show="isErrorResponse">
            <v-col cols="12" align="center">
              <p style="color:red;">
                There was an error while sending your data. Try again.
              </p>
            </v-col>
          </v-row>
          <v-row v-show="isSuccessfulResponse">
            <v-col cols="12" align="center">
              <p>
                Your data has been successfully submitted.
              </p>
              <p>Your submission ID is {{ this.submissionId }}.</p>
              <p>
                It will be available when processed
                <router-link :to="`/visualise-data/${this.submissionId}`"
                  >here</router-link
                >.
              </p>
            </v-col>
          </v-row>
          <v-row v-show="isInputBoxShown">
            <v-col cols="2"></v-col>
            <v-col cols="8" align="center">
              <v-textarea
                v-model="text"
                solo
                name="textinput-textarea"
                id="textinput-textarea"
                label="Paste here book text for analysis"
              ></v-textarea>
            </v-col>
            <v-col cols="2"></v-col>
          </v-row>
          <v-row v-show="isInputBoxShown">
            <v-col cols="12" align="center">
              <p style="margin-bottom: 10px;">
                or upload a file below. Supported files: txt, pdf.
              </p>
              <label id="text-reader">
                READ FILE
                <input
                  id="textinput-file"
                  type="file"
                  @change="loadTextFromFile"
                />
              </label>
            </v-col>
          </v-row>
          <v-row v-show="isInputBoxShown">
            <v-col cols="12" align="center">
              <v-btn color="success" v-on:click="submitData"
                >Send for analysis</v-btn
              >
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import pdfjsLib from "pdfjs-dist";
import axios from "axios";

export default {
  data: () => ({
    text: "",
    isLoading: false,
    fullPage: true,
    isInputBoxShown: true,
    isErrorResponse: false,
    isSuccessfulResponse: false,
    submissionId: -1
  }),
  methods: {
    loadTextFromFile(ev) {
      this.isLoading = true;
      const file = ev.target.files[0];
      const reader = new FileReader();

      setTimeout(() => {
        this.isLoading = false;
        this.onCancel();
      }, 50000);

      if (file.type.match("text/*")) {
        reader.onloadend = e => {
          this.text = e.target.result;
          this.isLoading = false;
        };

        reader.readAsText(file);
      } else if (file.type.match("application/pdf")) {
        reader.onloadend = e => {
          this.convertPdf(e.target.result);
        };

        reader.readAsDataURL(file);
      } else {
        console.log("unsupported file");
        this.isLoading = false;
      }
    },
    onCancel() {
      console.log("User cancelled the loader.");
    },
    async convertPdf(base64EncodedPdf) {
      const base64EncodedPdfArr = base64EncodedPdf.split(",");
      base64EncodedPdf = base64EncodedPdfArr[1];
      const pdfData = atob(base64EncodedPdf);
      const pdfText = await this.getPdfText(pdfData);
      this.text = pdfText;
      this.isLoading = false;
    },
    async getPdfText(data) {
      const doc = await pdfjsLib.getDocument({ data }).promise;
      const pageTexts = Array.from({ length: doc.numPages }, async (v, i) => {
        return (await (await doc.getPage(i + 1)).getTextContent()).items
          .map(token => token.str)
          .join(" ");
      });
      return (await Promise.all(pageTexts)).join("\n");
    },
    submitData(ev) {
      this.isLoading = true;
      this.isInputBoxShown = false;
      this.isErrorResponse = false;
      return axios
        .post(
          "http://127.0.0.1:5000/methodOne",
          { name: "test", text: this.text }, // TODO: add field for text name input
          {
            headers: {
              "Content-type": "application/json"
            }
          }
        )
        .then(response => {
          this.submissionId = response.data;
          this.isSuccessfulResponse = true;
          this.isLoading = false;
        })
        .catch(error => {
          console.log("error: " + error);
          this.isInputBoxShown = true;
          this.isErrorResponse = true;
          this.isLoading = false;
        });
    }
  },
  components: {
    Loading
  }
};
</script>

<style>
#textinput-textarea {
  width: 60%;
  height: 500px;
}

#text-reader {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 5px;
  padding: 6px 12px;
  cursor: pointer;
  background-color: #2196f3;
  font-size: 14px;
  color: white;
  font-weight: 500;
}

#text-reader input {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  opacity: 0;
}
</style>
