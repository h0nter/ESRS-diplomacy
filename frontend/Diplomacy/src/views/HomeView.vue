<template>
  <div class="h-full w-full flex flex-col items-center justify-center gap-4">
    <h1 class="text-4xl">Welcome to ESRS-Diplomacy</h1>
    <p class="text-xl">To play, either Log in or create an account</p>
    <div class="flex gap-10">
      <router-link
        to="/login"
        class="w-40 bg-emerald-600 p-3 rounded-lg font-bold hover:bg-emerald-500 text-center"
      >
        Log In
      </router-link>
      <router-link
        to="/register"
        class="w-40 bg-emerald-600 p-3 rounded-lg font-bold hover:bg-emerald-500 text-center"
      >
        Register
      </router-link>
    </div>
  </div>
</template>

<script setup></script>

<style></style>
