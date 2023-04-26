<template>
  <div class="px-4 pa-2 mt-10">
    <div class="d-flex justify-space-between align-center">
      <div class="left">
        <div class="text-h4 mt-2 cyan--text">ಪ್ರತಿಕ್ರಿಯೆ</div>
        <div class="my-2">
          ನಿಮ್ಮ ಅಭಿಪ್ರಾಯವನ್ನು ನಾವು ಗೌರವಿಸುತ್ತೇವೆ ಮತ್ತು ನಿಮ್ಮ ಆಲೋಚನೆಗಳನ್ನು
          ನಮ್ಮೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಲು ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುವುದನ್ನು ನಾವು ಪ್ರಶಂಸಿಸುತ್ತೇವೆ.
        </div>
      </div>
      <div class="right">
        <v-btn @click="handleClick()">ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ</v-btn>
      </div>
    </div>
    <v-divider></v-divider>
    <v-alert
      v-if="loading"
      icon="mdi-loading"
      class="mt-3"
      type="warning"
      title=""
      text=""
      >ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ ...</v-alert
    >
    <v-alert
      v-if="feedbacks.length === 0"
      class="mt-3"
      type="info"
      title=""
      text=""
      >ಯಾವುದೇ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಇನ್ನೂ ಹಂಚಿಕೊಂಡಿಲ್ಲ !</v-alert
    >
    <div v-else>
      <div v-for="(feedback, index) in feedbacks" :key="index">
        <v-card class="my-3" color="#385F73" dark>
          <v-card-title class="text-h5"> {{ feedback.uname }} </v-card-title>
          <v-card-subtitle>{{ feedback.feedback }}</v-card-subtitle>
        </v-card>
      </div>
    </div>
    <v-dialog v-model="dialog" width="auto">
      <v-card class="pa-5">
        <div class="text-h4 cyan--text">ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ</div>
        <div class="py-3">
          ನಿಮ್ಮ ಅಭಿಪ್ರಾಯವನ್ನು ನಾವು ಗೌರವಿಸುತ್ತೇವೆ ಮತ್ತು ನಿಮ್ಮ ಅಭಿಪ್ರಾಯವನ್ನು
          ಹಂಚಿಕೊಳ್ಳಲು ನೀವು ಸಮಯವನ್ನು ತೆಗೆದುಕೊಳ್ಳುವುದನ್ನು ಪ್ರಶಂಸಿಸುತ್ತೇವೆ
          ನಮ್ಮೊಂದಿಗೆ ಆಲೋಚನೆಗಳು. ನಮ್ಮದನ್ನು ಸುಧಾರಿಸಲು ನಮಗೆ ಸಹಾಯ ಮಾಡುವಲ್ಲಿ ನಿಮ್ಮ
          ಪ್ರತಿಕ್ರಿಯೆ ಮುಖ್ಯವಾಗಿದೆ ನಿಮ್ಮ ಅಗತ್ಯಗಳನ್ನು ಉತ್ತಮವಾಗಿ ಪೂರೈಸಲು ಉತ್ಪನ್ನಗಳು
          ಮತ್ತು ಸೇವೆಗಳು. ದಯವಿಟ್ಟು ಫಾರ್ಮ್ ಅನ್ನು ಬಳಸಿ ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆ,
          ಕಾಮೆಂಟ್‌ಗಳು, ಸಲಹೆಗಳು ಅಥವಾ ಯಾವುದೇ ಸಮಸ್ಯೆಗಳನ್ನು ಒದಗಿಸಲು ಕೆಳಗೆ ನೀವು
          ಅನುಭವಿಸಿರಬಹುದು.
        </div>
        <v-divider></v-divider>
        <div class="pt-3">
          <v-text-field
            label="ಹೆಸರು"
            :disabled="saving"
            filled
            v-model="uname"
          ></v-text-field>
          <v-textarea
            label="ರತಿಕ್ರಿಯೆ"
            filled
            :disabled="saving"
            v-model="newFeedback"
          ></v-textarea>
        </div>
        <v-divider></v-divider>
        <div class="d-flex mt-4">
          <v-btn
            color="cyan"
            text
            :disabled="saving"
            class="white--text ml-auto mr-2"
            @click="handleClick()"
            >ರದ್ದುಮಾಡು</v-btn
          >
          <v-btn
            color="cyan"
            :disabled="saving"
            :loading="saving"
            class="white--text"
            @click="saveFeedback()"
            >ಪಾಲು</v-btn
          >
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      loading: false,
      saving: false,
      uname: "",
      newFeedback: "",
      feedbacks: [],
    };
  },
  methods: {
    handleClick() {
      this.dialog = !this.dialog;
    },
    saveFeedback() {
      this.saving = true;
      this.$store
        .dispatch("uploadFeedback", {
          uname: this.uname,
          feedback: this.newFeedback,
        })
        .then((resp) => {
          window.location.reload(true);
        })
        .catch((err) => {
          console.log(err);
          this.saving = false;
        });
      this.handleClick();
    },
  },
  created() {
    this.loading = true;
    this.feedbacks = [];
    this.$store
      .dispatch("downloadFeedback")
      .then((resp) => {
        this.loading = false;
        resp.forEach((doc) => {
          this.feedbacks.push({ id: doc.id, ...doc.data() });
        });
      })
      .catch((err) => {
        console.log(err);
        this.loading = false;
      });
  },
};
</script>

<style lang="scss" scoped>
</style>