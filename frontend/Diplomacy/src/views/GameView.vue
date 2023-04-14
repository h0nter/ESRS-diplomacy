<template>
  <ButtonRouterLink :to="RouteNames.HOME" text="Home" />
  <Map />
</template>

<script setup>

import Container from "@/App.vue";
import Header from "@/components/Header.vue";
import ButtonRouterLink from "@/components/ButtonRouterLink.vue";
import Map from "@/components/Map.vue";
import {RouteNames} from "@/router/RouteNames";
</script>

<style scoped>

</style>