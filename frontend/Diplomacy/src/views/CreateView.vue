<template>
  <div class="h-full w-full flex flex-col items-center justify-center">
    <div class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg">
      <h1 class="text-4xl font-bold text-center">Create a game</h1>
      <div class="flex flex-col gap-6 my-6">
        <div>
          <p class="pl-3">Name:</p>
          <input
            type="text"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
            placeholder="Game name"
          />
        </div>
        <div>
          <p class="pl-3">Map:</p>
          <select
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg border-r-[12px] border-transparent"
            placeholder="Game name"
          >
            <option value="">Europe</option>
            <option value="">Asia</option>
            <option value="">America</option>
            <option value="">World</option>
          </select>
        </div>
        <div>
          <p class="pl-3">Visibility:</p>
          <div class="flex justify-around gap-4">
            <label
              class="flex-1 flex flex-row-reverse justify-center items-center gap-2 bg-slate-600 p-3 rounded-lg hover:bg-slate-500 cursor-pointer select-none radioselector"
              ><p class="flex-1">Public</p>
              <input
                type="radio"
                name="visibility"
                checked="checked"
                class="hidden absolute"
              />
              <span class="h-4 w-4 bg-slate-400 rounded-sm checkmark"></span>
            </label>
            <label
              class="flex-1 flex flex-row-reverse justify-center items-center gap-2 bg-slate-600 p-3 rounded-lg hover:bg-slate-500 cursor-pointer select-none radioselector"
              ><p class="flex-1">Private</p>
              <input type="radio" name="visibility" class="hidden absolute" />
              <span class="h-4 w-4 bg-slate-400 rounded-sm checkmark"></span>
            </label>
          </div>
        </div>
        <div>
          <p class="pl-3">Max players:</p>
          <input
            type="number"
            value="8"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
            placeholder="0"
          />
        </div>
        <button
          class="p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
  .radioselector input:checked ~ .checkmark {
    @apply bg-emerald-500;
  }

  .checkmark:after {
    @apply absolute hidden;
    content: "";
  }

  .radioselector input:checked ~ .checkmark:after {
    @apply block;
  }

  .radioselector .checkmark:after {
    @apply w-2 h-2 bg-emerald-200 top-1 left-1 rounded-sm;
  }
</style>
