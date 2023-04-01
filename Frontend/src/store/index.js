import Vue from "vue";
import Vuex from "vuex";

import {
  getFirestore,
  doc,
  onSnapshot,
  setDoc,
  addDoc,
  collection,
  getDoc,
  getDocs,
  orderBy,
  query,
  deleteDoc,
  updateDoc,
} from "firebase/firestore";

import {
  getDownloadURL,
  getStorage,
  ref,
  uploadBytes,
  deleteObject,
  listAll,
} from "firebase/storage";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {
    // Upload Data
    async uploadFile(context, payload) {
      const storageRef = ref(
        getStorage(),
        "authors/" +
          payload.author +
          "/" +
          Date.now() +
          payload.file.name.split(".")[0] +
          ".txt"
      );
      return new Promise((resolve, reject) => {
        try {
          uploadBytes(storageRef, payload.file)
            .then((snapshot) => {
              resolve(snapshot);
            })
            .catch((err) => {
              reject(err);
            });
        } catch (err) {
          reject(err);
        }
      });
    },

    async uploadDoc(context, payload) {
      return new Promise((resolve, reject) => {
        addDoc(collection(getFirestore(), "authors"), {
          name: payload,
          timestamp: Date.now(),
        })
          .then((resp) => {
            resolve(resp.id);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },

    async uploadFeedback(context, payload) {
      return new Promise((resolve, reject) => {
        addDoc(collection(getFirestore(), "feedback"), {
          uname: payload.uname,
          feedback: payload.feedback,
          timestamp: Date.now(),
        })
          .then((resp) => {
            resolve(resp.id);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },

    // Download Data
    async downloadCollection(context, payload) {
      return new Promise((resolve, reject) => {
        const collectionRef = collection(getFirestore(), "authors");
        getDocs(collectionRef)
          .then((querySnapshot) => {
            resolve(querySnapshot);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },

    async downloadFeedback(context, payload) {
      return new Promise((resolve, reject) => {
        const collectionRef = collection(getFirestore(), "feedback");
        getDocs(collectionRef)
          .then((querySnapshot) => {
            resolve(querySnapshot);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },

    async listAllFiles(context) {
      const sortedFiles = [];
      return new Promise((resolve, reject) => {
        listAll(ref(getStorage(), "authors"))
          .then((authors) => {
            authors.prefixes.forEach((author) => {
              const downloadUrls = [];
              listAll(ref(getStorage(), author.fullPath)).then((files) => {
                files.items.forEach((file) => {
                  getDownloadURL(ref(getStorage(), file.fullPath)).then(
                    (downloadUrl) => {
                      downloadUrls.push({ filename: file.name, downloadUrl });
                    }
                  );
                });
              });
              sortedFiles.push({
                author: author.name,
                downloadUrls,
              });
            });
            resolve(sortedFiles);
          })
          .catch((error) => {
            console.log(error);
            reject(error);
          });
      });
    },
  },
  modules: {},
});
