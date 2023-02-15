import {createApp, h, provide} from "vue";

import {apolloClient} from "@/apollo-config";
import {ApolloClients} from "@vue/apollo-composable";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

import "./index.css";

const app = createApp({
  setup() {
    provide(ApolloClients, {
      default: apolloClient,
    });
  },
  render: () => h(App),
});

app.use(router);

app.mount("#app");
