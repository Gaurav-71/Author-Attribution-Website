<template>
  <v-app>
    <Header />
    <v-main>
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
</style>
