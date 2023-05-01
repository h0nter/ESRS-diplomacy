<template>
  <div
    class="hamburger absolute p-4 m-0 left-6 top-6 rounded-full flex flex-col gap-[5px] hover:cursor-pointer z-50 hover:shadow-lg hover:bg-slate-200"
    :class="{ open: isMenuOpen }"
    @click="toggleMenu"
  >
    <span class="hamburger-top"></span>
    <span class="hamburger-middle"></span>
    <span class="hamburger-bottom"></span>
  </div>
  <div
    class="bg-blue-100 inline-block overflow-hidden mt-20 transition-width absolute z-40"
    :class="isMenuOpen ? 'w-auto' : 'w-0'"
  >
    <ul>
      <router-link to="/" class="block">Home</router-link>
      <router-link to="/join" class="block">Join Game</router-link>
      <router-link to="/create" class="block">Create Game</router-link>
      <router-link to="/game" class="block">Active Games</router-link>
      <router-link to="/login" class="block">Login</router-link>
      <router-link to="/register" class="block">Register</router-link>
      <router-link to="/settings" class="block">Settings</router-link>
    </ul>
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
      console.log("toggleMenu");
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
};
</script>

<style scoped>
.hamburger-top,
.hamburger-middle,
.hamburger-bottom {
  background-color: #000;
  display: block;
  height: 2px;
  transition: all 0.3s ease-in-out;
  width: 20px;
}

.open .hamburger-top {
  transform: rotate(45deg) translate(2px, 8px);
}

.open .hamburger-middle {
  opacity: 0;
}

.open .hamburger-bottom {
  transform: rotate(-45deg) translate(2px, -8px);
}
</style>
