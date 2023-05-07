<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <h1 class="text-3xl">Join a game with code</h1>
    <div class="mt-4">
      <input
        type="text"
        class="px-4 py-2 rounded-lg rounded-r-none bg-slate-700 focus:bg-slate-600 focus:outline-none"
        placeholder="Game code"
      />
      <button
        class="bg-emerald-600 px-4 py-2 rounded-lg rounded-l-none hover:bg-emerald-500"
      >
        Join
      </button>
    </div>
    <h1 class="text-3xl mt-8">Or join a public game</h1>

    <div class="w-3/5 mt-4 grid grid-cols-7 gap-4">
      <p class="col-span-2 text-lg font-bold">Name:</p>
      <p class="text-lg font-bold">Host:</p>
      <p class="text-lg font-bold">Map:</p>
      <p class="text-lg font-bold">Players:</p>
      <p class="text-lg font-bold">Created:</p>
    </div>
    <div
      v-for="game in games"
      class="w-3/5 grid grid-cols-7 gap-4 p-8 mt-4 bg-slate-700 box-content items-center rounded-xl hover:bg-slate-600"
    >
      <p class="col-span-2 text-lg">{{ game.name }}</p>
      <p class="text-lg">{{ game.host }}</p>
      <p class="text-lg">{{ game.map }}</p>
      <p class="text-lg">{{ game.players }} / {{ game.maxPlayers }}</p>
      <p class="text-lg">{{ game.created }}</p>
      <router-link
        to="/lobby"
        class="bg-emerald-600 px-4 py-2 rounded-lg text-lg hover:bg-emerald-500 text-center"
      >
        Join
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
  let games = [
    {
      name: "Bestest game ever, come join plz",
      host: "Artur",
      map: "Europe",
      players: "8",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test2",
      host: "Artur",
      map: "Europe",
      players: "5",
      maxPlayers: "6",
      created: "12/12/2021",
    },
    {
      name: "test3",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test4",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test2",
      host: "Artur",
      map: "Europe",
      players: "5",
      maxPlayers: "6",
      created: "12/12/2021",
    },
    {
      name: "test3",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test4",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test3",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
    {
      name: "test4",
      host: "Artur",
      map: "Europe",
      players: "2",
      maxPlayers: "8",
      created: "12/12/2021",
    },
  ];
</script>

<style scoped></style>
