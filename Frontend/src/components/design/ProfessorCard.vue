<template>
  <v-card>
    <div class="img-container">
      <v-img :src="imgAddr(data.imgName)"></v-img>
    </div>
    <div class="card-body">
      <div class="text-h6 px-3">{{ data.name }}</div>
      <div class="caption px-3">{{ data.role }}</div>
      <div class="px-3 pt-3 caption">
        {{ data.designation }}
      </div>
      <v-img
        class="mt-4"
        width="130"
        height="40"
        src="../../assets/random/rit.png"
      ></v-img>
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    data: Object,
  },
  data() {
    return {};
  },
  methods: {
    imgAddr(filename) {
      return require("../../assets/professors/" + filename + ".png");
    },
  },
};
</script>

<style lang="scss" scoped>
.v-card {
  width: 30rem;
  height: 12rem;
  display: flex;
  margin-right: 3rem;
  overflow: hidden;
  .card-body {
    padding: 1rem;
  }
}
</style>