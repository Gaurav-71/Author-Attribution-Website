<template>
  <div class="prediction">
    <v-tabs v-model="tab">
      <v-tab>All</v-tab>
      <v-tab>Profile based approach</v-tab>
      <v-tab>Bi-directional LSTM approach</v-tab>
      <v-tab>Instance based approach</v-tab>
      <v-tab>Compression based approach</v-tab>
      <v-tab>Graph based approach</v-tab>
    </v-tabs>
    <v-tabs-items class="pa-5" v-model="tab">
      <v-tab-item>
        <v-form>
          <v-textarea
            background-color="blue-grey lighten-4"
            color="black"
            outlined
            name="text"
            label="Kannada Input Text"
            height="350"
            v-model="kannadaText"
            :value="kannadaText"
            clearable
          ></v-textarea>
          <div class="btn-container">
            <v-btn class="cyan--text">Predict Author</v-btn>
          </div>
        </v-form>
      </v-tab-item>
      <v-tab-item></v-tab-item>
      <v-tab-item></v-tab-item>
      <v-tab-item></v-tab-item>
      <v-tab-item></v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tab: null,
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