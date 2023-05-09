<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <div v-if="hostError" class="text-red-600">{{ hostErrorM }}</div>
    <div v-else-if="hostLoading" class="text-slate-50">Loading...</div>
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
          <p v-if="hostRoom?.room_code">
            {{ hostRoom?.room_code }}
          </p>
          <p>Lobby Name:</p>
          <p v-if="hostRoom?.room_name">
            {{ hostRoom?.room_name }}
          </p>
          <p>Map:</p>
          <p>Europe</p>
          <p>Visibility:</p>
          <p>Public</p>
          <p>Players:</p>
          <p v-if="player_loading">... / 7</p>
          <p v-else>{{ players?.length }} / 7</p>
        </div>
      </div>
      <div class="bg-slate-700 p-4">
        <button
          v-if="hostRoom?.hoster.toString() === authStore.userID"
          class="w-full p-3 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-600 rounded-lg font-bold"
          :disabled="game_loading"
          v-html="game_loading ? 'Loading...' : 'Start Game'"
          @click="startGame"
        ></button>
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
  import router from "@/router";
  import { RoomStatus } from "@/models/API_support";
  import { useGameStore } from "@/stores/GameStore";
  import { API_URL, useInitGameStore } from "@/stores/InitGameStore";
  import { storeToRefs } from "pinia";

  const REFRESH_RATE = 3000;

  const authStore = useAuthStore();
  const initGameStore = useInitGameStore();
  const { hostRoom, hostLoading, hostError, hostErrorM } =
    storeToRefs(initGameStore);
  const gameStore = useGameStore();

  // Get the host ID from the route
  const route = useRoute();
  const host_id = String(route.params.id);

  initGameStore.fetchHostRoom(parseInt(host_id), false);

  const error = ref(false);
  const errorM = ref("");

  // Reload players data from the API every REFRESH_RATE
  // Prepare data and config for the request
  const players = ref<PlayerData[]>();

  const player_loading = ref(false);

  const pl_req_data = new FormData();
  pl_req_data.append("host_id", host_id);

  const players_config = {
    method: "post",
    url: API_URL + "/player_list/",
    data: pl_req_data,
  };

  // Setup the interval variable for cleanup in onUnmounted
  // eslint-disable-next-line no-undef
  let players_interval: NodeJS.Timeout = null;

  // Handle starting the game if the user isn't the host
  // Prepare data and config for the request
  const hs_req_data = new FormData();
  hs_req_data.append("host_id", host_id);

  const host_status_config = {
    method: "post",
    url: API_URL + "/host_status/",
    data: hs_req_data,
  };

  // Setup the interval variable for cleanup in onUnmounted
  // eslint-disable-next-line no-undef
  let host_status_interval: NodeJS.Timeout = null;

  // Start the intervals on component mount
  onMounted(() => {
    // Interval for reloading players
    players_interval = setInterval(() => {
      player_loading.value = true;
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
    }, REFRESH_RATE);

    // Interval for checking the room status and redirecting to the game
    if (hostRoom.value?.hoster.toString() !== authStore.userID) {
      host_status_interval = setInterval(() => {
        axios(host_status_config)
          .then((response) => {
            const status = response.data?.status;
            if (status === RoomStatus.INITIALIZE) {
              // Redirect user to the game
              router.push({
                name: "game",
                params: { host_id: host_id, room_id: response.data?.room_id },
              });
              return;
            }
          })
          .catch((err) => {
            error.value = true;
            errorM.value = err;
          });
      }, REFRESH_RATE);
    }
  });

  // Clean up the intervals on component unmount
  onUnmounted(() => {
    clearInterval(players_interval);
    if (host_status_interval !== null) clearInterval(host_status_interval);
  });

  // Handle game start if user is the host
  // Game loading status
  const game_loading = ref(false);

  const startGame = () => {
    const data = new FormData();
    data.append("host_id", host_id);

    const start_config = {
      method: "post",
      url: API_URL + "/start_game/",
      data: data,
    };

    game_loading.value = true;

    axios(start_config)
      .then((response) => {
        console.log(response.data);
        // If start successful, redirect to game
        const room_id = response.data?.data?.createRoom?.room?.id;
        if (room_id) {
          // Redirect user to the game
          router.push({
            name: "game",
            params: { host_id: host_id, room_id: room_id },
          });
          game_loading.value = false;
          return;
        }
        // If start unsuccessful, show error
        error.value = true;
        errorM.value =
          "There was a problem starting your game. Please try again.";
        game_loading.value = false;
      })
      .catch((err) => {
        error.value = true;
        errorM.value = err;
        console.log(err);
        game_loading.value = false;
      });
  };
</script>
