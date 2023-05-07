<template>
  <div class="h-full w-full flex justify-center items-center">
    <div class="w-1/3 bg-slate-700 p-6 shadow-md rounded-lg">
      <h1 class="text-4xl font-bold text-center">Register</h1>
      <div class="flex flex-col gap-6 my-6">
        <div>
          <p class="pl-3">Email:</p>
          <input
            type="text"
            placeholder="Email"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Username:</p>
          <input
            type="text"
            placeholder="Username"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Password:</p>
          <input
            type="password"
            placeholder="Password"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <div>
          <p class="pl-3">Re-enter Password:</p>
          <input
            type="password"
            placeholder="Re-enter Password"
            class="bg-slate-600 focus:bg-slate-500 focus:outline-none p-3 w-full rounded-lg"
          />
        </div>
        <button
          class="p-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold"
        >
          Register
        </button>
      </div>
      <div class="text-center">
        <p class="inline">Already a member?</p>
        <router-link class="text-blue-400" to="/login"> Log in</router-link>
      </div>
    </div>
  </div>
</template>

<script setup></script>
