<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <div v-if="error" class="text-red-600">{{ errorM }}</div>
    <div v-else-if="loading" class="text-slate-50">Loading...</div>
    <h1 v-else class="text-3xl">{{ hostRoom?.room_name }}</h1>
  </div>
  <div class="w-3/5 grid grid-cols-3 m-auto gap-4">
    <div class="col-span-2 bg-slate-700 p-8">
      <h1 class="text-2xl text-center">Players:</h1>
      <div class="flex flex-col gap-6 mt-4">
        <div
          v-for="player in players"
          :key="player.user_id"
          class="bg-slate-600 p-4 rounded-lg"
        >
          <p class="text-xl">{{ player.username }}</p>
        </div>
      </div>
    </div>
    <div class="flex flex-col justify-between">
      <div class="bg-slate-700 p-8">
        <h3 class="text-center text-2xl">Lobby Data</h3>
        <div class="grid grid-cols-2 mt-4 gap-y-4">
          <p>Game Code:</p>
          <p v-if="hostRoom?.room_code">{{ hostRoom?.room_code }}</p>
          <p>Lobby Name:</p>
          <p v-if="hostRoom?.room_name">{{ hostRoom?.room_name }}</p>
          <p>Map:</p>
          <p>Europe</p>
          <p>Visibility:</p>
          <p>Public</p>
          <p>Players:</p>
          <p v-if="loading">... / 7</p>
          <p v-else>{{ players?.length }} / 7</p>
        </div>
      </div>
      <div class="bg-slate-700 p-4">
        <button
          v-if="hostRoom?.hoster.toString() === authStore.userID"
          class="w-full p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
          @click="startGame"
        >
          Start Game
        </button>
        <button
          v-else
          class="w-full p-3 disabled:bg-slate-600 rounded-lg font-bold"
          disabled
        >
          Awaiting Host to Start the Game
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { useRoute } from "vue-router";
  import axios from "axios";
  import { useAuthStore } from "@/stores/AuthStore";
  import { onMounted, onUnmounted, ref } from "vue";
  import type { HostData, PlayerData } from "@/models/API_support";

  const authStore = useAuthStore();

  const route = useRoute();
  const host_id = String(route.params.id);

  const hostRoom = ref<HostData>();

  const host_loading = ref(false);
  const error = ref(false);
  const errorM = ref("");

  const host_config = {
    method: "get",
    url: "http://127.0.0.1:8000/api/host/",
  };

  host_loading.value = true;

  axios(host_config)
    .then((response) => {
      // Get the room data from the response
      const allHosts: HostData[] = response.data;

      hostRoom.value = allHosts.find((host) => host.id.toString() === host_id);

      host_loading.value = false;
    })
    .catch((err) => {
      error.value = true;
      errorM.value = err;
      console.log(err);
      host_loading.value = false;
    });

  const players = ref<PlayerData[]>();

  const player_loading = ref(false);
  const player_error = ref(false);
  const player_errorM = ref("");

  const pl_req_data = new FormData();
  pl_req_data.append("host_id", host_id);

  const players_config = {
    method: "post",
    url: "http://127.0.0.1:8000/api/player_list/",
    data: pl_req_data,
  };

  player_loading.value = true;

  // eslint-disable-next-line no-undef
  let players_interval: NodeJS.Timeout = null;

  onMounted(() => {
    players_interval = setInterval(() => {
      axios(players_config)
        .then((response) => {
          players.value = response.data;

          player_loading.value = false;
        })
        .catch((err) => {
          error.value = true;
          errorM.value = err;
          player_loading.value = false;
        });
    }, 3000);
  });

  onUnmounted(() => {
    clearInterval(players_interval);
  });
</script>
