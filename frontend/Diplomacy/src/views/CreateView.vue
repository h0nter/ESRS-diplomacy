<template>
  <div class="h-full w-full flex flex-col items-center justify-center">
    <div class="border border-black p-4">
      <h1 class="text-3xl">Create a game</h1>
      <div>
        <p>Name:</p>
        <input
          type="text"
          class="px-4 py-2 rounded-lg border border-black"
          placeholder="Game name"
        />
        <p>Map:</p>
        <select
          class="px-4 py-2 rounded-lg border border-black"
          placeholder="Game name"
        >
          <option value="">Europe</option>
          <option value="">Asia</option>
          <option value="">America</option>
          <option value="">World</option>
        </select>
        <p>Private:</p>
        <input
          type="checkbox"
          class="px-4 py-2 rounded-lg border border-black"
        />
        <p>Max players:</p>
        <input
          type="number"
          class="px-4 py-2 rounded-lg border border-black"
          placeholder="0"
        />
        <button
          class="block bg-blue-200 w-full mt-4 px-4 py-2 rounded-lg border border-black hover:bg-blue-400"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
p {
  @apply mt-4;
}
</style>
