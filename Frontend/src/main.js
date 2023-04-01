import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyDW-dNXVkyNYuUOTzbVFI5O873Duxd4A3o",
  authDomain: "authorattribution.firebaseapp.com",
  projectId: "authorattribution",
  storageBucket: "authorattribution.appspot.com",
  messagingSenderId: "475816124401",
  appId: "1:475816124401:web:607b0e37dc20c8c9d02e50",
  measurementId: "G-FW4NG0X1YQ",
};

Vue.config.productionTip = false;

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
