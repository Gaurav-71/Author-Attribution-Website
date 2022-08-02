<template>
  <v-card>
    <div class="img-container">
      <img :src="imgAddr(data.imgName)" />
    </div>
    <div class="card-body">
      <div class="text-h6 px-3 cyan--text text-center">{{ data.title }}</div>
      <v-card-text>
        <div class="text-center">
          {{ data.description }}
        </div>
      </v-card-text>
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
      return require("../../assets/about/" + filename + ".png");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../scss/main.scss";
.v-card {
  width: 16rem;
  height: 24rem;
  display: grid;
  grid-auto-rows: 45% auto;
  overflow: hidden;
  .img-container {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: $header-bg;
    border-radius: 50%;
    img {
      width: 90px;
      height: 90px;
    }
  }
  .card-body {
    // background: $background;
    // border-radius: 20%;
    padding-top: 1rem;
  }
}
</style>