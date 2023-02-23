<template>
<RouterLink v-bind:to="url" class="btn btn-blue">
  {{ text }}
</RouterLink>
</template>

<script setup>
const props = defineProps({
  url: String,
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