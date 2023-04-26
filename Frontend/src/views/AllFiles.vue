<template>
  <div class="all-files">
    <v-btn @click="downloadAll" :loading="loading" :disabled="loading"
      >ಡೇಟಾಸೆಟ್‌ಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ</v-btn
    >
  </div>
</template>

<script>
import axios from "axios";
import JSZip from "jszip";
import { saveAs } from "file-saver";
export default {
  data() {
    return {
      authors: [],
      loading: false,
    };
  },
  methods: {
    async downloadAll() {
      for (let j = 0; j < this.authors.length; j++) {
        const name = this.authors[j].author;
        const urls = this.authors[j].downloadUrls;
        console.log(urls.length);
        var zip = new JSZip();
        var files = zip.folder(name);
        let fileCounter = 0;
        for (let i = 0; i < urls.length; i++) {
          console.log("in l2");
          axios({
            url: urls[i].downloadUrl,
            method: "GET",
            responseType: "blob",
          }).then((resp) => {
            console.log("in then");
            fileCounter += 1;
            console.log(fileCounter, urls.length);
            files.file(urls[i].filename, resp.data);
            if (fileCounter == urls.length) {
              console.log("in if");
              files.generateAsync({ type: "blob" }).then(function (content) {
                saveAs(content, name + ".zip");
              });
            }
          });
        }
      }
    },
  },
  created() {
    this.loading = true;
    this.$store.dispatch("listAllFiles").then((resp) => {
      this.authors = resp;
      this.loading = false;
    });
  },
};
</script>

<style>
</style>