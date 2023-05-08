<template>
  <div class="h-full w-full flex justify-center items-center">
    <div v-if="!loading" class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg">
      <h1 class="text-4xl font-bold text-center">Register</h1>
      <div class="flex flex-col gap-6 my-6">
        <div>
          <p class="pl-3">Email:</p>
          <input
            type="text"
            placeholder="Email"
            v-model="email"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Username:</p>
          <input
            type="text"
            placeholder="Username"
            v-model="username"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Password:</p>
          <input
            type="password"
            placeholder="Password"
            v-model="password"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Re-enter Password:</p>
          <input
            type="password"
            placeholder="Re-enter Password"
            v-model="password2"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <button
          @click="register"
          class="p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
        >
          Register
        </button>
      </div>
      <div class="mb-4 -mt-4" v-if="error">
        <p class="text-center font-bold text-red-600" v-html="errorM"></p>
      </div>
      <div class="text-center">
        <p class="inline">Already a member?</p>
        <router-link class="text-blue-400" to="/login"> Log in</router-link>
      </div>
    </div>
    <div v-if="loading" class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg">
      <Spinner></Spinner>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "@/stores/AuthStore";

  const email = ref("");
  const username = ref("");
  const password = ref("");
  const password2 = ref("");
  const loading = ref(false);
  const error = ref(false);
  const errorM = ref("");

  const authStore = useAuthStore();

  const router = useRouter();

  let register = async () => {
    if (password.value !== password2.value) {
      error.value = true;
      errorM.value = "Passwords do not match";
      return;
    }

    if (email.value === "") {
      error.value = true;
      errorM.value = "Email may not be empty";
      return;
    }

    loading.value = true;

    try {
      await authStore.register(email.value, username.value, password.value);
      router.replace("/join");
    } catch (err) {
      error.value = true;
      errorM.value = err;
    }

    loading.value = false;
  };
</script>
