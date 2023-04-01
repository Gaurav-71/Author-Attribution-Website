<template>
  <div class="px-4 pa-2">
    <div class="d-flex justify-space-between align-center">
      <div class="left">
        <div class="text-h4 mt-2 cyan--text">Feedback</div>
        <div class="my-2">
          We value your opinion and appreciate you taking the time to share your
          thoughts with us.
        </div>
      </div>
      <div class="right">
        <v-btn @click="handleClick()">Share Feedback</v-btn>
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
      >Loading Feedback ...</v-alert
    >
    <v-alert
      v-if="feedbacks.length === 0"
      class="mt-3"
      type="info"
      title=""
      text=""
      >No feedback shared yet !</v-alert
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
        <div class="text-h4 cyan--text">Share Feedback</div>
        <div class="py-3">
          We value your opinion and appreciate you taking the time to share your
          thoughts with us. Your feedback is important in helping us improve our
          products and services to better meet your needs. Please use the form
          below to provide your feedback, comments, suggestions, or any issues
          you may have experienced.
        </div>
        <v-divider></v-divider>
        <div class="pt-3">
          <v-text-field
            label="uname"
            :disabled="saving"
            filled
            v-model="uname"
          ></v-text-field>
          <v-textarea
            label="Feedback"
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
            >Cancel</v-btn
          >
          <v-btn
            color="cyan"
            :disabled="saving"
            :loading="saving"
            class="white--text"
            @click="saveFeedback()"
            >Share</v-btn
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