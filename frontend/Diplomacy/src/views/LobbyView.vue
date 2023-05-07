<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <h1 class="text-3xl">Bestest game ever, come join plz</h1>
  </div>
  <div class="w-3/5 grid grid-cols-3 m-auto gap-4">
    <div class="col-span-2 bg-slate-700 p-8">
      <h1 class="text-2xl text-center">Players:</h1>
      <div class="flex flex-col gap-6 mt-4">
        <div v-for="player in players" class="bg-slate-600 p-4 rounded-lg">
          <p class="text-xl">{{ player.username }}</p>
        </div>
      </div>
    </div>
    <div class="flex flex-col justify-between">
      <div class="bg-slate-700 p-8">
        <h3 class="text-center text-2xl">Lobby Data</h3>
        <div class="grid grid-cols-2 mt-4 gap-y-4">
          <p v-if="true">Game Code:</p>
          <p v-if="true">ABCDEF</p>
          <p>Lobby Name:</p>
          <p>Bestest game ever, come join plz</p>
          <p>Map:</p>
          <p>Europe</p>
          <p>Visibility:</p>
          <p>Public</p>
          <p>Players:</p>
          <p>6/8</p>
        </div>
      </div>
      <div class="bg-slate-700 p-4">
        <button
          class="w-full p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
        >
          Start Game
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
let players = [
  {
    username: "Artur",
  },
  {
    username: "Henry",
  },
  {
    username: "Joe",
  },
  {
    username: "Josh",
  },
  {
    username: "Niels",
  },
  {
    username: "Tym",
  },
];
</script>
