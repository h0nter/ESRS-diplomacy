<template>
  <header>
    <h1>{{ title }}</h1>
  </header>
</template>

<script setup>
  const props = defineProps({
    title: String,
  });
</script>

<style scoped>
  header {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  h1 {
    font-size: 4rem;
    font-weight: bold;
    text-align: center;
  }
</style>
