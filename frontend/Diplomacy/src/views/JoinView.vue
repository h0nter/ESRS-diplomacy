<template>
  <div class="pt-24 pb-4 flex flex-col items-center w-full">
    <h1 class="text-3xl">Join a game with code</h1>
    <div class="mt-4">
      <input
        type="text"
        class="px-4 py-2 rounded-lg rounded-r-none bg-slate-700 focus:bg-slate-600 focus:outline-none"
        placeholder="Game code"
      />
      <button
        class="bg-emerald-600 px-4 py-2 rounded-lg rounded-l-none hover:bg-emerald-500"
      >
        Join
      </button>
    </div>
    <h1 class="text-3xl mt-8">Or join a public game</h1>

    <div
      v-if="loading"
      class="w-1/3 mt-4 bg-slate-700 p-6 shadow-md rounded-lg"
    >
      <Spinner></Spinner>
    </div>

    <div
      v-if="!loading && error"
      class="w-1/3 mt-4 bg-slate-700 p-6 shadow-md rounded-lg"
    >
      <p class="text-center font-bold text-red-600" v-html="errorM"></p>
    </div>

    <div
      v-if="!loading && !error && games.length === 0"
      class="w-1/3 mt-4 bg-slate-700 p-6 shadow-md rounded-lg flex flex-col items-center gap-4"
    >
      <p class="text-center">
        There are no open games. Start playing by creating one
      </p>
      <router-link
        to="/create"
        class="w-40 bg-emerald-600 p-3 rounded-lg font-bold hover:bg-emerald-500 text-center"
      >
        Create
      </router-link>
    </div>

    <div
      v-if="!loading && !error && games.length > 0"
      class="w-3/5 mt-4 flex flex-col items-center"
    >
      <div class="w-full grid grid-cols-7 gap-4">
        <p class="col-span-2 text-lg font-bold">Name:</p>
        <p class="text-lg font-bold">Host:</p>
        <p class="text-lg font-bold">Map:</p>
        <p class="text-lg font-bold">Players:</p>
        <p class="text-lg font-bold">Created:</p>
      </div>
      <div
        v-for="game in games"
        class="w-full grid grid-cols-7 gap-4 p-8 mt-4 bg-slate-700 box-content items-center rounded-xl hover:bg-slate-600"
      >
        <p class="col-span-2 text-lg">{{ game.name }}</p>
        <p class="text-lg">{{ game.host }}</p>
        <p class="text-lg">{{ game.map }}</p>
        <p class="text-lg">{{ game.players }} / {{ game.maxPlayers }}</p>
        <p class="text-lg">{{ game.created }}</p>
        <button
          @click="joinGame(game.id)"
          class="bg-emerald-600 px-4 py-2 rounded-lg text-lg hover:bg-emerald-500 text-center"
        >
          Join
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "@/stores/AuthStore";
  import axios from "axios";
  import { RoomStatus } from "@/models/API_support";

  const API_URL = import.meta.env.VITE_HOST_URL + "/api";

  interface game {
    id: string;
    name: string;
    host: string;
    map: string;
    players: string;
    maxPlayers: string;
    created: string;
  }

  const loading = ref(true);
  const error = ref(false);
  const errorM = ref("");
  const games = ref<Array<game>>([]);

  const authStore = useAuthStore();
  const router = useRouter();

  const config = {
    method: "get",
    url: API_URL + "/host/",
  };

  axios(config)
    .then((response) => {
      let loadedGames: Array<game> = [];
      response.data.forEach((data) => {
        if (data.status != RoomStatus.REGISTERED) {
          return;
        }
        let newGame = {
          id: data.id,
          name: data.room_name,
          host: data.hoster,
          map: "Europe",
          players: "X",
          maxPlayers: data.max_players,
          created: "can't fetch",
        };
        loadedGames.push(newGame);
      });
      games.value = loadedGames;
      loading.value = false;
    })
    .catch((e) => {
      error.value = true;
      errorM.value = "Could not fetch games";
      loading.value = false;
      console.log(loading.value);
    });

  async function joinGame(id: string) {
    // Get the list of players in the game
    const pl_req_data = new FormData();
    pl_req_data.append("host_id", id);

    const pl_req_config = {
      method: "post",
      url: API_URL + "/player_list/",
      data: pl_req_data,
    };

    let joined = false;

    // Fetch the list - if we can't load it, abandon the join
    const response = await axios(pl_req_config).catch(function (error) {
      alert("Failed to join game");
    });

    // Check if the user is already in the game
    response?.data.filter((data) => {
      if (data.user_id.toString() === authStore.userID) {
        // If the user is already in the game, redirect to the lobby
        router.push("/lobby/" + id + "/");
        joined = true;
      }
    });

    // If redirecting to the lobby, don't join the game
    if (joined) return;

    const join_req_data = new FormData();
    join_req_data.append("host", id);
    join_req_data.append("user", authStore.userID);

    const join_req_config = {
      method: "post",
      url: API_URL + "/player/",
      data: join_req_data,
    };

    axios(join_req_config)
      .then(function (response) {
        router.push("/lobby/" + id + "/");
      })
      .catch(function (error) {
        alert("Failed to join game");
      });
  }
</script>

<style scoped></style>
