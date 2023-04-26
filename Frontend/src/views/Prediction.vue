<template>
  <div class="prediction mt-10">
    <v-tabs v-model="tab">
      <v-tab class="cyan--text">ಎಲ್ಲಾ</v-tab>
      <v-tab class="cyan--text">ಎನ್ಗ್ರಾಮ್ ವಿಧಾನ</v-tab>
      <v-tab class="cyan--text">ಸಂಕೋಚನ ವಿಧಾನ</v-tab>
      <!-- <v-tab class="cyan--text">LSTM approach</v-tab> -->
      <v-tab class="cyan--text">ಲೆಕ್ಸಿಕಲ್ ವಿಧಾನ</v-tab>
      <v-tab class="cyan--text">ಭಾವನೆ ಪಾಲಿಸೋಮ್ ವಿಧಾನ</v-tab>
    </v-tabs>
    <v-tabs-items class="pa-5" v-model="tab">
      <v-tab-item> <All /></v-tab-item>
      <v-tab-item><Approach type="ngram" /></v-tab-item>
      <v-tab-item><Approach type="compression" /></v-tab-item>
      <!-- <v-tab-item><Approach type="na" /></v-tab-item> -->
      <v-tab-item><Approach type="lexical" /></v-tab-item>
      <v-tab-item><Approach type="polysemy" /></v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import All from "../components/design/All.vue";
import Approach from "../components/design/Approach.vue";
export default {
  components: {
    Approach,
    All,
  },
  data() {
    return {
      tab: 0,
      kannadaText: "",
    };
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
</style>