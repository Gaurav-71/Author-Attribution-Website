<template>
  <div class="wip" v-if="approachType == 'na'">
    <img src="../../assets/random/wip.svg" alt="work in progress" />
    <div class="text-h4">
      We are working on deploying this approach, please try again later !
    </div>
  </div>
  <div v-else class="approach">
    <div class="text-h4 mb-3">{{ titleString() }}</div>
    <v-divider class="mb-5"></v-divider>
    <div v-if="isLoading"><Loading /></div>
    <div v-else>
      <v-form v-if="!prediction">
        <v-textarea
          background-color="blue-grey lighten-4"
          color="cyan darken-1"
          outlined
          name="text"
          label="ಕನ್ನಡ ಇನ್‌ಪುಟ್ ಪಠ್ಯ"
          height="350"
          v-model="kannadaText"
          :value="kannadaText"
          prepend-inner-icon="mdi-text"
          clearable
        ></v-textarea>
        <div class="btn-container">
          <v-file-input
            color="cyan"
            accept=".txt"
            chips
            prepend-icon="mdi-cloud-upload"
            label="ಫೈಲ್ ಅಪ್ಲೋಡ್ ಮಾಡಿ"
            class="cyan--text"
            @change="fileUpload()"
            @click:clear="clear()"
            v-model="file"
          ></v-file-input>

          <div class="btns">
            <!-- <v-btn @click="copyText()" class="mr-3 cyan--text" text
              ><v-icon class="mr-3">mdi-content-copy</v-icon>Copy sample text to
              clipboard
            </v-btn> -->
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn class="mr-3 cyan--text" text v-bind="attrs" v-on="on"
                  ><v-icon class="mr-3">mdi-content-copy</v-icon>ಮಾದರಿಯನ್ನು
                  ನಕಲಿಸಿ ಕ್ಲಿಪ್‌ಬೋರ್ಡ್‌ಗೆ ಪಠ್ಯ
                </v-btn>
              </template>
              <v-list v-for="(author, index) in authors" :key="index">
                <v-list-item :key="index" @click="copyText(index + 1)">
                  {{ author }}
                </v-list-item>
                <v-divider v-if="index != authors.length - 1"></v-divider>
              </v-list>
            </v-menu>

            <v-btn @click="predictAuthor()" class="cyan--text"
              ><v-icon class="mr-2">mdi-chart-timeline-variant-shimmer</v-icon
              >ಲೇಖಕರನ್ನು ಗುರುತಿಶಸಿ</v-btn
            >
          </div>
        </div>
      </v-form>
      <div v-else class="results">
        <div class="text-h5 cyan--text mb-3">ಇನ್ಪುಟ್ ಪಠ್ಯ</div>
        <div translate="no" class="notranslate">
          {{ limitText(kannadaText) }}
        </div>
        <div class="text-h5 cyan--text mt-5 mb-3">ಫಲಿತಾಂಶಗಳು</div>
        <div class="author-name d-flex">
          <b class="mr-1">ಲೇಖಕರ ಹೆಸರು</b> :
          {{ formatName(prediction.Author_Name) }}
        </div>
        <div class="accuracy">
          <b>ಮುನ್ಸೂಚನೆಯ ನಿಖರತೆ</b> :
          {{ formatAccuracy(prediction.Accuracy) }}
        </div>
        <v-divider class="mt-8"></v-divider>
        <v-btn @click="reset()" dark class="mt-6 cyan"
          ><v-icon class="mr-3">mdi-reload</v-icon> ಮತ್ತೆ ಪ್ರಯತ್ನಿಸು</v-btn
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Loading from "./Loading.vue";
import { baseUrl } from "../../Constants";
import { text1, text2, text3, text4, authors } from "./SampleText";

export default {
  components: { Loading },
  props: {
    type: String,
  },
  data() {
    return {
      approachType: this.type,
      kannadaText: "",
      prediction: null,
      isLoading: false,
      file: null,
      content: null,
      authors: authors,
    };
  },
  methods: {
    titleString() {
      switch (this.approachType) {
        case "ngram":
          return "ಎನ್-ಗ್ರಾಮ್ ಅಪ್ರೋಚ್";
        case "compression":
          return "ಕಂಪ್ರೆಷನ್ ಅಪ್ರೋಚ್";
        case "lstm":
          return "LSTM Approach";
        case "lexical":
          return "ಲೆಕ್ಸಿಕಲ್ ಅಪ್ರೋಚ್";
        case "polysemy":
          return "ಭಾವನೆ ಪಾಲಿಸೋಮ್ ಅಪ್ರೋಚ್";
      }
    },
    predictAuthor() {
      this.isLoading = true;
      var formData = new FormData();
      formData.append("kannada_text", this.kannadaText);
      axios({
        method: "POST",
        url: baseUrl + this.approachType,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((resp) => {
          this.prediction = resp.data;
          this.isLoading = false;
        })
        .catch((err) => {
          console.log("err" + err);
          alert(err);
          this.isLoading = false;
        });
    },
    formatName(authorName) {
      var words = authorName.split("_");
      var CapitalizedWords = [];
      words.forEach((element) => {
        CapitalizedWords.push(
          element[0].toUpperCase() + element.slice(1, element.length)
        );
      });
      return CapitalizedWords.join(" ");
    },
    formatAccuracy(accuracy) {
      let res = accuracy * 100;
      return res.toFixed(2).toString() + "%";
    },
    reset() {
      this.clear();
      this.prediction = null;
      this.isLoading = false;
    },
    limitText(text) {
      if (text.length > 350) {
        return text.substring(0, 350) + " ...";
      } else {
        return text;
      }
    },
    copyText(type) {
      let text = "";
      switch (type) {
        case 1:
          text = text1;
          break;
        case 2:
          text = text2;
          break;
        case 3:
          text = text3;
          break;
        case 4:
          text = text4;
          break;
      }
      navigator.clipboard
        .writeText(text)
        .then()
        .catch((err) => {
          console.log(err);
        });
      this.kannadaText = text;
    },
    fileUpload() {
      const reader = new FileReader();
      try {
        if (this.file.name.includes(".txt")) {
          reader.onload = (res) => {
            this.content = res.target.result;
            this.kannadaText = this.content;
          };
          reader.onerror = (err) => console.log(err);
          reader.readAsText(this.file);
        }
      } catch (err) {}
    },
    clear() {
      this.content = null;
      this.kannadaText = null;
      this.file = null;
    },
  },
};
</script>

<style lang="scss" scoped>
.btn-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wip {
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  img {
    width: auto;
    height: 60vh;
  }
}

.btns {
  display: flex;
  align-items: center;
}

.v-file-input {
  max-width: 200px;
}
</style>