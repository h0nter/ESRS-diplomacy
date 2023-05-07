<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <h1 class="text-3xl">Your Currently Active Games:</h1>

    <div
      v-if="false"
      class="flex flex-col items-center justify-center gap-4 mt-4"
    >
      <h2 class="text-xl">
        You don't have any active games. You can start playing by joining a
        lobby or creating one
      </h2>
      <div class="flex gap-10">
        <router-link
          to="/login"
          class="w-40 bg-emerald-600 p-3 rounded-lg font-bold hover:bg-emerald-500 text-center"
        >
          Join A Lobby
        </router-link>
        <router-link
          to="/register"
          class="w-40 bg-emerald-600 p-3 rounded-lg font-bold hover:bg-emerald-500 text-center"
        >
          Create A Lobby
        </router-link>
      </div>
    </div>
    <div v-if="true" class="w-3/5 mt-4 grid grid-cols-5 gap-4">
      <p class="col-span-2 text-lg font-bold">Name:</p>
      <p class="text-lg font-bold">Status:</p>
      <p class="text-lg font-bold">Time Left:</p>
    </div>
    <div
      v-for="game in games"
      class="w-3/5 grid grid-cols-5 gap-4 p-8 mt-4 bg-slate-700 box-content items-center rounded-xl hover:bg-slate-600"
    >
      <p class="col-span-2 text-lg">{{ game.name }}</p>
      <p class="text-lg">{{ game.status }}</p>
      <p class="text-lg">{{ game.timeleft }}</p>
      <router-link
        to="/game"
        class="bg-emerald-600 px-4 py-2 rounded-lg text-lg hover:bg-emerald-500 text-center"
      >
        Enter
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { RouterLink } from "vue-router";

  let games = [
    {
      name: "Bestest game ever, come join plz",
      status: "Waiting To Start",
      timeleft: "N/A",
    },
    {
      name: "Testing5",
      status: "Orders Submitted",
      timeleft: "12m15s",
    },
    {
      name: "Risk v2.0",
      status: "Awaiting Orders",
      timeleft: "1h12m5s",
    },
    {
      name: "Is this game any good?",
      status: "Orders Submitted",
      timeleft: "2m30s",
    },
  ];
</script>

<style scoped></style>
