<template>
  <div class="h-full w-full flex flex-col items-center justify-center">
    <div class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg" v-if="!loading">
      <h1 class="text-4xl font-bold text-center">Create a game</h1>
      <div class="flex flex-col gap-6 my-6">
        <div>
          <p class="pl-3">Name:</p>
          <input
            type="text"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
            placeholder="Game name"
            v-model.trim="name"
          />
        </div>
        <div>
          <p class="pl-3">Map:</p>
          <select
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg border-r-[12px] border-transparent"
            placeholder="Game name"
            v-model="map"
          >
            <option value="Europe" class="disabled:text-gray-400">
              Europe
            </option>
            <option value="Asia" class="disabled:text-gray-400" disabled>
              Asia
            </option>
            <option value="America" class="disabled:text-gray-400" disabled>
              America
            </option>
            <option value="World" class="disabled:text-gray-400" disabled>
              World
            </option>
          </select>
        </div>
        <div>
          <p class="pl-3">Visibility:</p>
          <div class="flex justify-around gap-4">
            <label
              class="flex-1 flex flex-row-reverse justify-center items-center gap-2 bg-slate-600 p-3 rounded-lg hover:bg-slate-500 cursor-pointer select-none radioselector"
              ><p class="flex-1">Public</p>
              <input
                type="radio"
                name="visibility"
                value="public"
                v-model="visibility"
                class="hidden absolute"
              />
              <span class="h-4 w-4 bg-slate-400 rounded-sm checkmark"></span>
            </label>
            <label
              class="flex-1 flex flex-row-reverse justify-center items-center gap-2 bg-slate-600 p-3 rounded-lg hover:bg-slate-500 cursor-pointer select-none radioselector"
              ><p class="flex-1">Private</p>
              <input
                type="radio"
                name="visibility"
                value="private"
                v-model="visibility"
                class="hidden absolute"
              />
              <span class="h-4 w-4 bg-slate-400 rounded-sm checkmark"></span>
            </label>
          </div>
        </div>
        <div>
          <p class="pl-3">Max players:</p>
          <input
            type="number"
            :min="minimumPlayers"
            :max="maximumPlayers"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
            placeholder="0"
            v-model="maxPlayers"
          />
        </div>
        <button
          class="p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
          @click="createGame"
        >
          Create
        </button>
        <div class="mb-4 -mt-4" v-if="error">
          <p class="text-center font-bold text-red-600" v-html="errorM"></p>
        </div>
      </div>
    </div>
    <div v-if="loading" class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg">
      <Spinner></Spinner>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "@/stores/AuthStore";
  import axios from "axios";

  const name = ref("");
  const map = ref("Europe");
  const visibility = ref("public");
  const maxPlayers = ref(7);
  const loading = ref(false);
  const error = ref(false);
  const errorM = ref("");

  const authStore = useAuthStore();
  const router = useRouter();

  const minimumPlayers = 2;
  const maximumPlayers = 7;

  function createGame() {
    if (name.value === "") {
      error.value = true;
      errorM.value = "Name cannot be empty";
      return;
    }

    if (
      maxPlayers.value < minimumPlayers ||
      maxPlayers.value > maximumPlayers
    ) {
      error.value = true;
      errorM.value =
        "Max players must be between " +
        minimumPlayers +
        " and " +
        maximumPlayers;
      return;
    }

    let data = new FormData();
    data.append("room_name", name.value);
    data.append("hoster", authStore.userID);

    let config = {
      method: "post",
      url: "http://127.0.0.1:8000/api/host/",
      data: data,
    };

    loading.value = true;

    axios(config)
      .then((response) => {
        let data = new FormData();
        data.append("room_id", response.data.id);

        var config = {
          method: "post",
          url: "http://127.0.0.1:8000/api/start_game/",
          data: data,
        };

        axios(config)
          .then((response) => {
            console.log(response.data.data.createRoom.room.id);
            router.push("/lobby/" + response.data.data.createRoom.room.id);
          })
          .catch((err) => {
            error.value = true;
            errorM.value = err;
            console.log(err);
            loading.value = false;
          });
      })
      .catch((err) => {
        error.value = true;
        errorM.value = err;
        console.log(err);
        loading.value = false;
      });
  }
</script>

<style scoped>
  .radioselector input:checked ~ .checkmark {
    @apply bg-emerald-500;
  }

  .checkmark:after {
    @apply absolute hidden;
    content: "";
  }

  .radioselector input:checked ~ .checkmark:after {
    @apply block;
  }

  .radioselector .checkmark:after {
    @apply w-2 h-2 bg-emerald-200 top-1 left-1 rounded-sm;
  }
</style>
