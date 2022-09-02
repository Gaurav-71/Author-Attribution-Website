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
          <v-btn @click="copyText()" class="pl-0" text
            ><v-icon class="mr-3">mdi-content-copy</v-icon>Copy sample text to
            clipboard
          </v-btn>
          <div class="btns">
            <v-btn text class="cyan--text mr-4"
              ><v-icon class="mr-2">mdi-upload</v-icon> Upload file</v-btn
            >
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

import { Bar } from "vue-chartjs/legacy";

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
      results: {
        ngram: null,
        compression: null,
        // lstm: null,
        // lexical: null,
        // polysome: null,
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
        lstm: {
          Author_Name: "Gaurav Vinay",
          Accuracy: "0.9",
          Model: "lstm",
        },
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
          // "Lexical",
          // "Emotion Polysome",
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
    async predictAuthor() {
      this.isLoading = true;
      let baseUrl = "http://127.0.0.1:9090/";
      try {
        let ngram = await axios.post(baseUrl + "ngram", {
          kannada_text: this.kannadaText,
        });
        this.results.ngram = ngram.data;

        let compression = await axios.post(baseUrl + "compression", {
          kannada_text: this.kannadaText,
        });
        this.results.compression = compression.data;
        // add the other models here once it's complete
      } catch (err) {
        console.log("eeeeeeee", err);
        this.results = {
          ngram: null,
          compression: null,
          // lstm: null,
          // lexical: null,
          // polysome: null,
        };
      }
      this.chartData.datasets[0].data = [
        this.results.ngram.Accuracy * 100,
        this.results.compression.Accuracy * 100,
        // this.results.lstm.Accuracy * 100,
        // this.results.lexical.Accuracy * 100,
        // this.results.polysome.Accuracy * 100,
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
        case "lstm":
          return "LSTM";
        case "lexical":
          return "Lexical";
        case "emotion":
          return "Emotion Polysome";
      }
    },
    reset() {
      this.kannadaText = "";
      this.results = {
        ngram: null,
        compression: null,
        // lstm: null,
        // lexical: null,
        // polysome: null,
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
    copyText() {
      let text =
        "ಅದಕ್ಕೆ ಯಾಕೆ ನಾನು ಹಾಗೆ ಹೆಸರಿಟ್ಟೆನೋ ಗೊತ್ತಿಲ್ಲ. ಆಗಿನ್ನೂ ‘ಹಾಯ್ ಬೆಂಗಳೂರ್!’ ರೂಪು ತಳೆದಿರಲಿಲ್ಲ. ‘ಕರ್ಮವೀರ’ದಲ್ಲಿ ಇದ್ದೆ. ಮೊಟ್ಟ ಮೊದಲ ಸಂದರ್ಶನ ಬರೆಯುವ ಘಳಿಗೆಯಲ್ಲಿ, ಇದು ಎಲ್ಲೆಲ್ಲಿ ತಿರುಗಿ ಏನೇನು ರೂಪು ಪಡೆಯುತ್ತದೆಯೋ? ಗೊತ್ತಿರಲಿಲ್ಲ. ಒಂದು ಸಣ್ಣ ಮಳೆಯ ಇಳಿ ಸಂಜೆ ಶಿವಾಜಿನಗರದ ಕೋಳಿ ಅಂಗಡಿಯಲ್ಲಿ ನಾನು ಕೋಳಿ ಫಯಾಜ್‌ನನ್ನು ಭೇಟಿ ಮಾಡಿದ್ದೆ. ಕರೆದೊಯ್ದು ಪರಿಚಯಿಸಿದ್ದು ಗೆಳೆಯ ಸಿದ್ದೀಕ್ ಆಲ್ದೂರಿ. ಆತನಿಗಾದರೂ ಅಷ್ಟೆ. ಮುಂದೆ ಇದು ಯಾವ ರೂಪು ಪಡೆಯಲಿದೆ ಎಂಬ ಅಂದಾಜಿರಲಿಲ್ಲ. ಆಲ್ದೂರಿ ಆಗ ‘ಡೈಲಿ ಸಾಲಾರ್’ ನಲ್ಲಿ ವರದಿಗಾರನಾಗಿದ್ದ. ತುಂಬ ಸಜ್ಜನ ಆತ. ಕೋಳಿ ಫಯಾಜ್ ಕೂಡ ನನ್ನೊಂದಿಗೆ ಸಜ್ಜನನಾಗೇ ನಡೆದುಕೊಂಡ. ಫಯಾಜ್‌ನ ನಂತರ ನಾನು ಯಾರ‍್ಯಾರನ್ನು ಭೇಟಿ ಮಾಡಿದೆ, ಎಲ್ಲೆಲ್ಲಿ ಅಲೆದೆ ಎಂಬುದೆಲ್ಲ ಈಗ ಇತಿಹಾಸ. ನಾನು ‘ಕರ್ಮವೀರ’ದಿಂದ ಹೊರ ಬೀಳುವ ಹೊತ್ತಿಗೆ ಶ್ರೀರಾಂಪುರ ಕಿಟ್ಟಿ, ಕಾಲಾಪತ್ಥರ್, ಬಲರಾಮ, ಬೆಕ್ಕಣ್ಣು ರಾಜೇಂದ್ರ, ಜೇಡರಹಳ್ಳಿ ಕೃಷ್ಣಪ್ಪ- ಹೀಗೆ ಅನೇಕರನ್ನು ಭೇಟಿಯಾಗಿದ್ದೆ. ಕೆಲವರು ‘ಕರ್ಮವೀರ’ ಆಫೀಸಿಗೂ ಬಂದು ಹೋದರು. ಈ ಸಂದರ್ಶನದ ಸರಮಾಲೆಗೆ ‘ಪಾಪಿಗಳ ಲೋಕದಲ್ಲಿ’ ಅಂತ ಹೆಸರಿಟ್ಟೆ. ಹಾಗೇಕೆ ಇಟ್ಟೆನೋ? ಗೊತ್ತಿಲ್ಲ. ಇತ್ತೀಚೆಗೆ ಅದೇ ತರಹದ್ದಕ್ಕೆ ಕೈಹಾಕಿದೆ. ‘ಇದನ್ನೇನು ಮಾಡ್ತೀರಿ?’ ಎಂದು ಗೆಳೆಯರೊಬ್ಬರು ಕೇಳಿದರು. ಉತ್ತರ ನನಗೂ ಕೊಡಲಾಗಲಿಲ್ಲ. ಕೆಲವು ಸನ್ಯಾಸಿಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ಕಲೆ ಹಾಕುತ್ತಿದ್ದೆ. ‘ಕಾವಿಗಳ ಕೂಪದಲ್ಲಿ’ ಅಂತ ಹೆಸರಿಡಬಹುದು ನೋಡಿ, ಅಂದೆ. ಆತ ನಕ್ಕರು. ನಾನು ನಗಲಿಲ್ಲ. ಸುಮಾರು ಹದಿನೆಂಟು ವರ್ಷಗಳಷ್ಟು ಹಳೆಯ ನೋಟ್ಸ್  ನನ್ನಲ್ಲಿದೆ. ನಾನು ಬಯಲುಮಾಡಿದ ಮಾಡಿದ ಮೊಟ್ಟ ಮೊದಲನೆಯ ವಂಚಕ ಸ್ವಾಮಿ ಯಶವಂತಪುರದವನು ಇದು ಮಾರಕ ವರದಿಯಾಗಿದೆ. ‘ಪತ್ರಿಕೆ’ ಆಗಷ್ಟೆ ಆರಂಭವಾಗಿತ್ತು. ಯಶವಂತಪುರದಲ್ಲಿ ಬಿ.ಸಿ.ಪಾಟೀಲ್ ಸಬ್ ಇನ್ಸ್ ಪೆಕ್ಟರ್ ಆಗಿದ್ದರು. ಆಮೇಲೆ ಬಿಡಿ, ಅನೇಕರು ಬಯಲುಮಾಡಿದ ಆದರು. ನನ್ನ ವಧಾ ಸ್ಥಾನಕ್ಕೆ ಬಂದು ಹೋದರು. ಶಿರಸಿಯ ಒಬ್ಬ ಕಳ್ಳ ಸನ್ಯಾಸಿಯಂತೂ ‘ಪತ್ರಿಕೆ’ಯ ವರದಿಯಿಂದಾಗಿ ಬುಕ್ಕಾ ಫಕೀರನೇ ಆಗಿಹೋದ. ಅಂಥವರು ಅನೇಕರಿದ್ದಾರೆ. ಅದಲ್ಲ ಮುಖ್ಯ. ಸನ್ಯಾಸ, ದೇವಮಾನವ ಮುಂತಾದವು ಕೇವಲ ಕರ್ನಾಟಕದಲ್ಲಿಲ್ಲ. ಅದು ಜಾಗತಿಕ ಮಟ್ಟದ ಅಧ್ಯಯನ. ಓದಲು ಕುಳಿತರೆ ಆತಂಕವೇ ಆಗುತ್ತದೆ. ಮನುಕುಲಕ್ಕೆ ಎಂಥ ದರಿದ್ರ ಕೊಡುಗೆ ಇವರದು? ಪಕ್ಕದ ತಮಿಳುನಾಡಿನಲ್ಲಿ ದೇವಮಾನವನೆಂದು ಹೇಳಿಕೊಂಡು ಭಯಾನಕ ಕೃತ್ಯಗಳನ್ನೆಸಗಿದ ಒಬ್ಬ ಕಪಟಿ ಸ್ವಾಮಿಗೆ, ತುಂಬ ದಿಟ್ಟ ಹೆಣ್ಣು ಮಗಳಾದ ಭಾನುಮತಿ ಎಂಬ ನ್ಯಾಯಾಧೀಶೆ ಎರಡು ಜೀವಾವಧಿ ಶಿಕ್ಷೆ ನೀಡಿದರು. ಒಂದಾದ ಮೇಲೊಂದರಂತೆ ಎರಡು ಶಿಕ್ಷೆ ಅನುಭವಿಸಬೇಕು. ಅರವತ್ತೇಳು ಲಕ್ಷ ದಂಡ ಕಟ್ಟಬೇಕು. ಜೀವಾವಧಿಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಯಾವ ರಾಜಕೀಯ ಪಕ್ಷವೂ, ಸರ್ಕಾರವೂ ಈ ಪ್ರಕರಣದಲ್ಲಿ ತಲೆ ಹಾಕಬಾರದು ಅಂತ ಸ್ಪಷ್ಟವಾಗಿ ಬರೆದು ಆಕೆ ಎದ್ದು ಹೋದರು. ಶಿಕ್ಷೆ ಕಳೆಯುವ ಸಂಗತಿ ಹಾಗಿರಲಿ, ಜೈಲಿಗೆ ಹೋದ ಕೆಲವೇ ದಿನಗಳಲ್ಲಿ ಕಪಟಿ ಸನ್ಯಾಸಿ ಸತ್ತು ಹೋದ. ಅವನಿಗೆ ವಿಪರೀತ ದೊಡ್ಡ ಮಟ್ಟದ ರಾಜಕೀಯ ಸಂಪರ್ಕಗಳಿದ್ದವು. ಮೊನ್ನೆ ನಡೆದ ಸಸಾರಾಮ್ ಬಾಪು ಪ್ರಕರಣವನ್ನೇ ನೋಡಿ. ಅವನು ಒಂದು ಕಾಲು ಗೋರಿಯಲ್ಲಿಟ್ಟು ಕೊಂಡಿದ್ದಾನೆ. ಅಷ್ಟು ಮುದುಕ. ಅಂಥವನು ರೇಪ್ ಮಾಡುತ್ತಾನೆ. ಅವನ ಆಶ್ರಮದಲ್ಲಿ ಕೊಲೆಗಳಾಗಿವೆ. ಬಂಧಿಸಲು ಹೋದರೆ, ಪೊಲೀಸರನ್ನು ಭಕ್ತರು ಶತ್ರು ದೇಶದವರನ್ನು ತಡೆದಂತೆ ತಡೆದರು. ಕೊಡುವ ಜಾಗಕ್ಕೆ ಸರಿಯಾಗಿ ನಾಲ್ಕು ಬಾರಿಸಿ ಪೊಲೀಸರು ಮುದುಕನನ್ನು ಎಳೆದೊಯ್ದರು. ಮೊದಲೆಲ್ಲಾ ಹೀಗೆ ದೇವಮಾನವರು ಬಯಲು ಆಗುತ್ತಿರಲಿಲ್ಲ. ಅವರನ್ನು ಸಾಲುಗಟ್ಟಿ ಆಗ ಬಯಲಿಗೆಳೆದದ್ದು ಸರ್ದಾರ್ ಖುಷ್ವಂತ್‌ಸಿಂಗ್. ನಾನು ಅವರ ಬರಹಗಳಿಗಾಗಿಯೇ ‘ಇಲ್ಲ ಸ್ಟ್ರೇಟೆಡ್ ವೀಕ್ಲಿ’ ಓದುತ್ತಿದ್ದೆ. ಈ ದೇವಮಾನವರಿಗೆ ಒಂದೆರಡಲ್ಲ; ನಾನಾ ಟ್ರಿಕ್ಕುಗಳು ಗೊತ್ತಿವೆ. ರವಿಶಂಕರ್ ಗುರೂಜಿಯನ್ನೇ ನೋಡಿ. ಎಂಥೆಂಥವರನ್ನು ಪಳಗಿಸಿಟ್ಟುಕೊಂಡಿದ್ದಾನೆ. ಅವನು ದೇಶಗಳನ್ನು ಸುತ್ತುವರೆಯುವುದೇ ಒಂದು ಅಚ್ಚರಿ. ಇವತ್ತೋ-ನಾಳೆಯೋ ಒಂದು ನೊಬೆಲ್ ಪ್ರಶಸ್ತಿ ಬಂದರೆ ಆಶ್ಚರ್ಯ ಪಡಲೇ ಬೇಡಿ. ಬಂದರೆ ನನಗೆ ಬೇಸರವೇನೂ ಇಲ್ಲ. ಆದರೆ ಆತ ಆ ಪರಿ ಅಪಸ್ವರ ಹಾಡುತ್ತಾನೆ. ಹಾಡೋದು ಬಿಟ್ಟರೆ ಮಾತ್ರ ನೊಬೆಲ್ ಬಹುಮಾನ ಕೊಡ್ತೀವಿ ಅಂತ ಆ ಪ್ರತಿಷ್ಠಾನದವರು ಷರತ್ತು ಹಾಕಬೇಕು. ಇಂತಹವರ ಪ್ರಪಂಚವೇ ಬೇರೆ. ನಿಮಗೂ ಓದಲಿಕ್ಕೆ ರುಚಿಕರ ಅನ್ನಿಸೀತು. ‘ಕಾವಿಗಳ ಕೂಪದಲ್ಲಿ’ ಎಂಬ ಹೆಸರೂ ಸರಿಯಿದೆ, ಅಲ್ಲವೆ? ಕೆಲಸ ಮಾತ್ರ ಎದೆಗಿಂತ ಎತ್ತರ. ನೋಡೋಣ.";
      navigator.clipboard
        .writeText(text)
        .then()
        .catch((err) => {
          console.log(err);
        });
      this.kannadaText = text;
    },
  },
  created() {
    if (this.mock) {
      this.results = this.mockresults;
      this.chartData.datasets[0].data = [
        this.results.ngram.Accuracy * 100,
        this.results.compression.Accuracy * 100,
        this.results.lstm.Accuracy * 100,
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
</style>