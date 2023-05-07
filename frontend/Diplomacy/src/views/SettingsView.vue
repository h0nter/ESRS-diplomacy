<template>
  <div class="h-full w-full flex flex-col items-center">
    <div class="settingsSection">
      <h1 class="sectionHeader">General</h1>
      <h1>test1</h1>
    </div>
    <div class="settingsSection">
      <h1 class="sectionHeader">Security</h1>
      <h1>test1</h1>
      <h1>test1</h1>
    </div>
    <div class="settingsSection">
      <h1 class="sectionHeader">Danger zone!</h1>
      <h1>test1</h1>
      <h1>test1</h1>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
  .settingsSection {
    @apply border border-black rounded-xl w-3/4;
  }
  .sectionHeader {
    @apply text-3xl text-center p-2;
  }
</style>
