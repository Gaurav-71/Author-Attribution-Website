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
      <v-btn class="title-btn pl-2" text>ಕನ್ನಡ ಪಠ್ಯದ ಕರ್ತೃತ್ವ ಪರೀಕ್ಷೆ</v-btn>
    </div>
    <v-spacer></v-spacer>
    <div class="actions">
      <!-- <v-btn text><div id="google_translate_element"></div></v-btn> -->
      <v-btn to="/" text>ಮುಖಪುಟ</v-btn>
      <v-btn to="/datasets" text>ಡೇಟಾಸೆಟ್‌ಗಳು</v-btn>
      <v-btn to="/feedback" text>ಪ್ರತಿಕ್ರಿಯೆ</v-btn>
      <v-btn to="/prediction" rounded color="cyan">ಲೇಖಕರನ್ನು ಗುರುತಿಶಸಿ</v-btn>
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