import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const routes = [
    {
      path: "/",
      name: "home",
      component: HomeView,
      alias: "/home"
    },
    {
      path: "/game",
      name: "game",
      component: () => import("@/views/GameView.vue"),
    },
    // {
    //   path: '*',
    //   redirect: '/'
    // }

    // {
    //   path: "/about",
    //   name: "about",
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import("../views/AboutView.vue"),
    // },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
