<template>
  <div class="container lg:max-w-screen-lg px-5 py-5">
      <slot />
    </div>
</template>

<style scoped>
  .container{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>