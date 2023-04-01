import Vue from "vue";
import VueRouter from "vue-router";
import About from "../views/About.vue";
import Dataset from "../views/Dataset.vue";
import Prediction from "../views/Prediction.vue";
import Feedback from "../views/Feedback.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "about",
    component: About,
  },
  {
    path: "/datasets",
    name: "dataset",
    component: Dataset,
  },
  {
    path: "/prediction",
    name: "prediction",
    component: Prediction,
  },
  {
    path: "/feedback",
    name: "feedback",
    component: Feedback,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
