<template>
<RouterLink v-bind:to="{name: to}" class="btn btn-blue">
  {{ text }}
</RouterLink>
</template>

<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  to: String,
  text: String
})
</script>

<style scoped>
  .btn {
    @apply font-bold py-2 px-4 mb-3 rounded;
  }
  .btn-blue {
    @apply bg-blue-500 text-white;
  }
  .btn-blue:hover {
    @apply bg-blue-700;
  }
</style>