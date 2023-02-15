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
    <Container>
      <RouterView/>
    </Container>
  </Wrapper>
</template>

<style>

  body{
    @apply bg-slate-50 text-slate-800 dark:bg-slate-800 dark:text-slate-50;
  }

</style>
