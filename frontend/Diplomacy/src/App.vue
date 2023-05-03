<script setup lang="ts">
import { RouterView } from "vue-router";
import DarkModeSwitch from "@/components/DarkModeSwitch.vue";
import Wrapper from "@/components/Wrapper.vue";
import Container from "@/components/Container.vue";
import Header from "@/components/Header.vue";
import ButtonRouterLink from "@/components/ButtonRouterLink.vue";
import HomeView from "@/views/HomeView.vue";
</script>

<template>
  <Wrapper>
    <DarkModeSwitch />
    <Container class="app-container">
      <RouterView/>
    </Container>
  </Wrapper>
</template>

<style scoped>
  .app-container{
    height: 100%;
  }
</style>
