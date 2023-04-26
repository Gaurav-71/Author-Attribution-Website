<template>
  <div class="dataset mt-10">
    <v-tabs v-model="tab">
      <v-tab class="cyan--text">ಅಪ್ಲೋಡ್</v-tab>
      <v-tab class="cyan--text">ಲೇಖಕರಿಂದ ವೀಕ್ಷಿಸಿ</v-tab>
    </v-tabs>
    <v-tabs-items class="pa-5" v-model="tab">
      <v-tab-item class="upload">
        <div class="left">
          <img src="../assets/random/upload.svg" alt="work in progress" />
        </div>
        <div class="right">
          <div class="flex">
            <div class="text-h4 mb-3 cyan--text">
              ಲೇಖಕರ ಫೈಲ್‌ಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ
            </div>
            <v-btn
              @click="toggleDialog"
              color="cyan"
              class="white--text py-4 mb-4 ml-3"
              >ಲೇಖಕರನ್ನು ರಚಿಸಿ</v-btn
            >
          </div>
          <v-divider></v-divider>
          <v-autocomplete
            label="ಲೇಖಕರನ್ನು ಆಯ್ಕೆ ಮಾಡಿ"
            class="mt-3"
            filled
            :loading="loading"
            :disabled="loading"
            v-model="author"
            :items="authors"
            item-text="name"
            item-value="id"
            messages="ಗಮನಿಸಿ : ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಲೇಖಕರ ಪಟ್ಟಿಯಲ್ಲಿ ಲೇಖಕರ ಹೆಸರು ಇಲ್ಲದಿದ್ದರೆ ದಯವಿಟ್ಟು ಹೊಸ ಲೇಖಕರನ್ನು ರಚಿಸಿ"
          ></v-autocomplete>
          <v-file-input
            show-size
            counter
            label=".txt ಫೈಲ್‌ಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ"
            placeholder="ಅಪ್‌ಲೋಡ್ ಮಾಡಲು ಫೈಲ್‌ಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ"
            class="mt-2"
            multiple
            filled
            color="cyan"
            accept=".txt"
            chips
            prepend-icon="mdi-cloud-upload"
            v-model="files"
          ></v-file-input>
          <div class="flex">
            <v-btn
              color="cyan white--text"
              class="ml-auto mt-4"
              @click="uploadFiles"
              >ಫೈಲ್‌ಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ</v-btn
            >
          </div>
          <v-dialog v-model="dialog" width="auto">
            <div class="pa-5 white" style="width: 80vw">
              <div class="text-h5 cyan--text">ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಹೊಸ ಲೇಖಕ</div>
              <div class="text-caption mb-4">
                ಹೊಸ ಲೇಖಕರನ್ನು ರಚಿಸುವುದು ಎಲ್ಲಾ ಸಂಬಂಧಿತ ಸಾಹಿತ್ಯವನ್ನು ಸಂಘಟಿಸಲು ಸಹಾಯ
                ಮಾಡುತ್ತದೆ ಒಟ್ಟಾಗಿ ಕೆಲಸಮಾಡಿ
              </div>
              <v-text-field
                label="ಲೇಖಕರ ಹೆಸರು"
                placeholder="ಲೇಖಕರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ"
                filled
                v-model="newAuthor"
                color="cyan"
              ></v-text-field>
              <v-btn color="cyan white--text" block @click="createAuthor"
                >ಲೇಖಕರನ್ನು ರಚಿಸಿ</v-btn
              >
            </div>
          </v-dialog>
        </div>
      </v-tab-item>
      <v-tab-item> <AllFiles /></v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import AllFiles from "./AllFiles.vue";
export default {
  components: { AllFiles },
  data() {
    return {
      tab: 0,
      dialog: false,
      loading: false,
      uploading: false,
      newAuthor: null,
      authors: [],
      author: null,
      files: [],
    };
  },
  methods: {
    toggleDialog() {
      this.dialog = !this.dialog;
      this.newAuthor = null;
    },
    createAuthor() {
      this.$store
        .dispatch("uploadDoc", this.newAuthor)
        .then(() => {
          this.uploading = false;
          this.toggleDialog();
          this.downloadAuthors();
        })
        .catch((err) => console.log(err));
    },
    uploadFiles() {
      for (let i = 0; i < this.files.length; i++) {
        const selectedAuthor = this.authors.find(
          (obj) => obj.id === this.author
        );
        console.log(selectedAuthor);
        this.$store.dispatch("uploadFile", {
          file: this.files[i],
          author: selectedAuthor.name + "(id:" + selectedAuthor.id + ")",
        });
        if (i == this.files.length - 1) {
          this.author = null;
          this.files = [];
        }
      }
    },
    downloadAuthors() {
      this.loading = true;
      this.authors = [];
      this.$store
        .dispatch("downloadCollection")
        .then((resp) => {
          this.loading = false;
          resp.forEach((doc) => {
            this.authors.push({ id: doc.id, ...doc.data() });
          });
        })
        .catch((err) => console.log(err));
    },
  },

  created() {
    this.downloadAuthors();
  },
};
</script>

<style lang="scss" scoped>
@import "../scss/main.scss";
.v-tabs-items {
  background: $body-bg !important;
  min-height: 90vh;
}
.btn-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-wrap: wrap;
  .left {
    display: flex;
    justify-content: center;
    align-items: center;
    img {
      width: 30%;
      height: auto;
    }
  }
  .right {
    width: 100%;
    margin-top: 2rem;
    .flex {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>