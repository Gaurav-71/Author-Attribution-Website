<template>
  <v-app>
    <Header />
    <v-main style="padding-top: 1.5rem">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Header from "./components/navigation/Header.vue";
export default {
  components: { Header },
  name: "App",

  data: () => ({
    //
  }),
};
</script>

<style lang="scss">
@import "./scss/main.scss";
.v-main {
  background-image: $body-bg;
}
.skiptranslate {
  position: fixed;
  bottom: 0;
  right: 0;
}

#google_translate_element {
  .skiptranslate {
    position: static;
    margin: 0 !important;
  }
}
</style>
