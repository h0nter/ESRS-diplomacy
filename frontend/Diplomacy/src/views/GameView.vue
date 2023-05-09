<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <p v-if="hostLoading" class="text-xl mb-4">Loading...</p>
    <h1 v-else class="text-3xl mb-4">{{ hostRoom?.room_name }}</h1>
    <p v-if="hostError" class="text-red-600 mb-4">{{ hostErrorM }}</p>
    <p v-else-if="hostLoading" class="text-xl mb-4">Loading...</p>
    <Map v-else />
  </div>
</template>

<script lang="ts" async setup>
  import Map from "@/components/Map.vue";
  import axios from "axios";
  import { useRoute } from "vue-router";
  import { API_URL, useInitGameStore } from "@/stores/InitGameStore";
  import { storeToRefs } from "pinia";
  import { useGameStore } from "@/stores/GameStore";
  import { HostData } from "@/models/API_support";
  import { ref } from "vue";

  const initGameStore = useInitGameStore();
  const { hostRoom, hostLoading, hostError, hostErrorM } =
    storeToRefs(initGameStore);
  const gameStore = useGameStore();

  // Get the host and room IDs from the route
  const route = useRoute();
  const host_id = String(route.params.host_id);
  const room_id = String(route.params.room_id);

  await initGameStore.fetchHostRoom(parseInt(host_id), true);

  const setNewGraphQLLink = () => {
    const room_ip = hostRoom.value?.ip;
    const room_port = hostRoom.value?.port;
    const url = `http://${room_ip}:${room_port}/graphql/`;

    gameStore.setNewGraphQLLink(url);
  };

  // Set the new GraphQL link when the host room is loaded
  setNewGraphQLLink();

  // Set the room id for the graphQL queries
  gameStore.roomID = parseInt(room_id);
</script>

<style scoped></style>
