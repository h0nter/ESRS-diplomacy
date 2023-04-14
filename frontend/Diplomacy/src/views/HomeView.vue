<template>
  <Header title="ESRS Diplomacy"/>
  <ButtonRouterLink :to="RouteNames.GAME" text="Start" />
</template>

<script setup>
  import Header from "@/components/Header.vue";
  import ButtonRouterLink from "@/components/ButtonRouterLink.vue";
  import {RouteNames} from "@/router/";
</script>

<style>

</style>