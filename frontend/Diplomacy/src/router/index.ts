import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    alias: "/home",
  },
  {
    path: "/join",
    name: "join",
    component: () => import("@/views/JoinView.vue"),
  },
  {
    path: "/create",
    name: "create",
    component: () => import("@/views/CreateView.vue"),
  },
  {
    path: "/game",
    name: "game",
    component: () => import("@/views/GameView.vue"),
  },

  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },

  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
  },

  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/SettingsView.vue"),
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
  routes,
});

export default router;
