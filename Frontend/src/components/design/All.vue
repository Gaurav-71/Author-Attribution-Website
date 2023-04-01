<template>
  <div class="approach">
    <div class="text-h4 mb-3">{{ titleString() }}</div>
    <v-divider class="mb-5"></v-divider>
    <div v-if="isLoading"><Loading /></div>
    <div v-else>
      <v-form v-if="!results.ngram">
        <v-textarea
          background-color="blue-grey lighten-4"
          color="cyan darken-1"
          outlined
          name="text"
          label="Kannada Input Text"
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
            label="Upload a File"
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
                  ><v-icon class="mr-3">mdi-content-copy</v-icon>Copy sample
                  text to clipboard
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
              >Predict Author</v-btn
            >
          </div>
        </div>
      </v-form>
      <div v-else class="results">
        <div class="text-h5 cyan--text mb-3">Input Text</div>
        {{ limitText(kannadaText) }}
        <div class="text-h5 cyan--text mt-5 mb-3">Results</div>
        <v-simple-table fixed-header dense>
          <template v-slot:default>
            <thead>
              <tr class="table-header">
                <th class="text-left">Model Name</th>
                <th class="text-left">Author Name</th>
                <th class="text-left">Model Accuracy</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(result, index) in results" :key="index">
                <td>{{ formatModelName(result.Model) }}</td>
                <td>{{ formatName(result.Author_Name) }}</td>
                <td>{{ formatAccuracy(result.Accuracy) }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
        <Bar
          class="mt-5"
          :chart-options="chartOptions"
          :chart-data="chartData"
        />
        <v-divider class="mt-8"></v-divider>
        <div class="d-flex justify-center">
          <v-btn @click="reset()" dark class="mt-6 cyan"
            ><v-icon class="mr-3">mdi-reload</v-icon> Try Again</v-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Loading from "./Loading.vue";
import { baseUrl } from "../../Constants";

import { Bar } from "vue-chartjs/legacy";

import { text1, text2, text3, text4, authors } from "./SampleText";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  components: { Loading, Bar },
  props: {
    type: String,
  },
  data() {
    return {
      mock: !true,
      approachType: this.type,
      kannadaText: "",
      isLoading: false,
      file: null,
      content: null,
      authors: authors,
      results: {
        ngram: null,
        compression: null,
        // lstm: null,
        lexical: null,
        polysome: null,
      },
      mockresults: {
        ngram: {
          Author_Name: "Gaurav Vinay",
          Accuracy: "0.99",
          Model: "ngram",
        },
        compression: {
          Author_Name: "Gaurav Vinay",
          Accuracy: "0.93",
          Model: "compression",
        },
        // lstm: {
        //   Author_Name: "Gaurav Vinay",
        //   Accuracy: "0.9",
        //   Model: "lstm",
        // },
        lexical: {
          Author_Name: "Gaurav Vinay",
          Accuracy: "1",
          Model: "lexical",
        },
        polysome: {
          Author_Name: "Gaurav Vinay",
          Accuracy: "0.80",
          Model: "emotion",
        },
      },
      chartData: {
        labels: [
          "N-gram",
          "Compression",
          // "LSTM",
          "Lexical",
          "Emotion Polysome",
        ],
        datasets: [
          {
            label: "Bar Graph",
            backgroundColor: [
              "#767B81",
              "#1D7874",
              "#679289",
              "#F4C095",
              "#EE646E",
            ],
            data: [],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  methods: {
    titleString() {
      return "Combined Approach";
    },
    generatePostObject(approachType) {
      var formData = new FormData();
      formData.append("kannada_text", this.kannadaText);
      return {
        method: "POST",
        url: baseUrl + approachType,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      };
    },
    async predictAuthor() {
      this.isLoading = true;
      try {
        let ngram = await axios(this.generatePostObject("ngram"));
        let compression = await axios(this.generatePostObject("compression"));
        let lexical = await axios(this.generatePostObject("lexical"));
        let polysome = await axios(this.generatePostObject("polysemy"));
        this.results.ngram = ngram.data;
        this.results.compression = compression.data;
        this.results.lexical = lexical.data;
        this.results.polysome = polysome.data;
      } catch (err) {
        console.log("error", err);
        this.results = {
          ngram: null,
          compression: null,
          // lstm: null,
          lexical: null,
          polysome: null,
        };
      }
      this.chartData.datasets[0].data = [
        this.results.ngram.Accuracy * 100,
        this.results.compression.Accuracy * 100,
        // this.results.compression.lstm * 100,
        this.results.lexical.Accuracy * 100,
        this.results.polysome.Accuracy * 100,
      ];
      this.isLoading = false;
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
    formatModelName(model) {
      switch (model) {
        case "ngram":
          return "N-gram";
        case "compression":
          return "Compression";
        // case "lstm":
        //   return "LSTM";
        case "Lexical Model":
          return "Lexical";
        case "Polysemy":
          return "Emotion Polysome";
      }
    },
    reset() {
      this.clear();
      this.results = {
        ngram: null,
        compression: null,
        // lstm: null,
        lexical: null,
        polysome: null,
      };
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
  created() {
    if (this.mock) {
      this.results = this.mockresults;
      this.chartData.datasets[0].data = [
        this.results.ngram.Accuracy * 100,
        this.results.compression.Accuracy * 100,
        // this.results.lstm.Accuracy * 100,
        this.results.lexical.Accuracy * 100,
        this.results.polysome.Accuracy * 100,
      ];
    }
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