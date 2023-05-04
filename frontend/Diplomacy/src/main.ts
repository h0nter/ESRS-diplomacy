import { createApp, h, provide } from "vue";

import { DefaultApolloClient } from "@vue/apollo-composable";
import { apolloClient } from "@/apollo-config";

import App from "./App.vue";
import router from "./router";

import { createPinia } from "pinia";

import "./assets/main.css";

import "./index.css";

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },
  render: () => h(App),
});

app.use(router);

const pinia = createPinia();
app.use(pinia);

app.mount("#app");
