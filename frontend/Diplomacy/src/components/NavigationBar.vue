<template>
  <div
    class="h-20 w-full flex fixed justify-center items-center bg-emerald-600 z-40"
  >
    <h1 class="text-4xl font-bold">ESRS Diplomacy</h1>
  </div>

  <div
    class="hamburger fixed p-4 m-0 left-4 top-4 rounded-full flex flex-col gap-[5px] hover:cursor-pointer z-50 hover:shadow-lg hover:bg-emerald-500"
    :class="{ open: isMenuOpen }"
    @click="toggleMenu"
  >
    <span class="hamburger-top"></span>
    <span class="hamburger-middle"></span>
    <span class="hamburger-bottom"></span>
  </div>

  <div
    class="navbar fixed flex flex-col justify-between left-0 top-20 bg-slate-700 overflow-hidden transition-width z-50"
    :class="isMenuOpen ? 'w-64' : 'w-0'"
  >
    <!-- DO NOTE, CAN USE MAX WIDTH TO ANIMATE INSTEAD -->
    <div>
      <router-link
        v-if="true"
        to="/login"
        class="navbar-link"
        @click="closeMenu"
        >Log In</router-link
      >
      <router-link
        v-if="true"
        to="/register"
        class="navbar-link"
        @click="closeMenu"
        >Register</router-link
      >
      <router-link v-if="true" to="/" class="navbar-link" @click="closeMenu"
        >Home</router-link
      >
      <router-link v-if="true" to="/join" class="navbar-link" @click="closeMenu"
        >Join Game</router-link
      >
      <router-link
        v-if="true"
        to="/create"
        class="navbar-link"
        @click="closeMenu"
        >Create Game</router-link
      >
      <router-link
        v-if="true"
        to="/active"
        class="navbar-link"
        @click="closeMenu"
        >Active Games</router-link
      >
      <router-link
        v-if="true"
        to="/settings"
        class="navbar-link"
        @click="closeMenu"
        >Settings</router-link
      >
    </div>
    <div>
      <router-link
        v-if="true"
        to="/settings"
        class="navbar-link"
        @click="closeMenu"
        >Log Out</router-link
      >
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
  },
};
</script>

<style scoped>
.hamburger-top,
.hamburger-middle,
.hamburger-bottom {
  background-color: #fff;
  display: block;
  height: 2px;
  transition: all 0.3s ease-in-out;
  width: 20px;
}

.open .hamburger-top {
  transform: rotate(45deg) translate(5px, 5px);
}

.open .hamburger-middle {
  opacity: 0;
}

.open .hamburger-bottom {
  transform: rotate(-45deg) translate(5px, -5px);
}

.navbar {
  height: calc(100vh - 5rem);
}

.navbar-link {
  @apply text-white block font-bold whitespace-nowrap py-4 px-6;
}

.navbar-link:hover {
  @apply bg-slate-500;
}

.arrow {
  border: solid black;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 3px;
}
</style>
