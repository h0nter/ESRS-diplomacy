<template>
  <div class="h-full w-full flex flex-col items-center">
    <h1 class="text-3xl">Join a game with code</h1>
    <div class="mt-4">
      <input
        type="text"
        class="px-4 py-2 rounded-lg rounded-r-none border border-black"
        placeholder="Game code"
      />
      <button
        class="bg-blue-200 px-4 py-2 rounded-lg rounded-l-none border border-black border-l-0 hover:bg-blue-400"
      >
        Join
      </button>
    </div>
    <h1 class="text-3xl mt-8">Or join a public game</h1>
    <table class="border border-black mt-4">
      <tr class="bg-slate-400">
        <th class="tableCell">Name</th>
        <th class="tableCell">Host</th>
        <th class="tableCell">Map</th>
        <th class="tableCell">Players</th>
        <th class="tableCell">Created</th>
        <th class="tableCell">Join</th>
      </tr>
      <tr
        v-for="game in games"
        :key="game.name"
        class="even:bg-gray-100 hover:bg-gray-200"
      >
        <td class="tableCell">{{ game.name }}</td>
        <td class="tableCell">{{ game.host }}</td>
        <td class="tableCell">{{ game.map }}</td>
        <td class="tableCell">{{ game.players }} / {{ game.maxPlayers }}</td>
        <td class="tableCell">{{ game.created }}</td>
        <td class="tableCell">
          <button
            class="bg-blue-200 px-4 py-2 rounded-lg border border-black hover:bg-blue-400"
          >
            Join
          </button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script setup lang="ts">
let games = [
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
];
</script>

<style scoped>
.tableCell {
  @apply p-4;
}
</style>
