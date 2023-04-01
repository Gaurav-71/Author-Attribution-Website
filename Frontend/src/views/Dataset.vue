<template>
  <div class="dataset">
    <v-tabs v-model="tab">
      <v-tab class="cyan--text">Upload</v-tab>
      <v-tab class="cyan--text">View by Author</v-tab>
    </v-tabs>
    <v-tabs-items class="pa-5" v-model="tab">
      <v-tab-item class="upload">
        <div class="left">
          <img src="../assets/random/upload.svg" alt="work in progress" />
        </div>
        <div class="right">
          <div class="flex">
            <div class="text-h4 mb-3 cyan--text">Upload Author Files</div>
            <v-btn
              @click="toggleDialog"
              color="cyan"
              class="white--text py-4 mb-4 ml-3"
              >Create Author</v-btn
            >
          </div>
          <v-divider></v-divider>
          <v-autocomplete
            label="Select Author"
            class="mt-3"
            filled
            :loading="loading"
            :disabled="loading"
            v-model="author"
            :items="authors"
            item-text="name"
            item-value="id"
            messages="Note : Please create a new author if author name is not in the existing list of authors"
          ></v-autocomplete>
          <v-file-input
            show-size
            counter
            label="Select .txt files"
            placeholder="Select files to upload"
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
              >Upload Files</v-btn
            >
          </div>
          <v-dialog v-model="dialog" width="auto">
            <div class="pa-5 white" style="width: 80vw">
              <div class="text-h5 cyan--text">New Author in Database</div>
              <div class="text-caption mb-4">
                Creating a new author helps in organising all related literary
                work together
              </div>
              <v-text-field
                label="Author name"
                placeholder="Enter author name"
                filled
                v-model="newAuthor"
                color="cyan"
              ></v-text-field>
              <v-btn color="cyan white--text" block @click="createAuthor"
                >Create Author</v-btn
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