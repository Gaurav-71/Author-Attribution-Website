<template>
  <v-app-bar class="header" app dark>
    <div class="logo d-flex align-center">
      <v-img
        alt="Logo"
        contain
        src="../../assets/logo/logo14.png"
        transition="scale-transition"
        width="50"
        height="50"
      />
      <v-btn class="title-btn pl-2" text
        >Author Attribution for Kannada Text</v-btn
      >
    </div>
    <v-spacer></v-spacer>
    <div class="actions">
      <v-btn text><div id="google_translate_element"></div></v-btn>
      <v-btn to="/" text>About</v-btn>
      <v-btn to="/datasets" text>Datasets</v-btn>
      <v-btn to="/feedback" text>Feedback</v-btn>
      <v-btn to="/prediction" rounded color="cyan">Prediction</v-btn>
    </div>
  </v-app-bar>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
@import "../../scss/main.scss";
.header {
  background-image: $header-bg;
  overflow: hidden;
  .actions {
    display: flex;
    align-items: center;
    .v-btn {
      margin: 0.5rem;
    }
  }
}
</style>