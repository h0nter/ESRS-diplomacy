import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/AuthStore";
import HomeView from "@/views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    alias: "/home",
    meta: { requiresAuth: false },
  },
  {
    path: "/join",
    name: "join",
    component: () => import("@/views/JoinView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/create",
    name: "create",
    component: () => import("@/views/CreateView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/active",
    name: "active",
    component: () => import("@/views/ActiveView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/lobby",
    name: "lobby",
    component: () => import("@/views/LobbyView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/game",
    name: "game",
    component: () => import("@/views/GameView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    meta: { requiresAuth: false },
  },

  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
    meta: { requiresAuth: false },
  },

  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/SettingsView.vue"),
    meta: { requiresAuth: true },
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

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.token) {
    next("/login");
  } else if (!to.meta.requiresAuth && authStore.token) {
    next("/join");
  } else {
    next();
  }
});

export default router;
