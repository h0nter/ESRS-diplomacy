<template>
  <div class="h-full w-full flex justify-center items-center">
    <div id="loginContainer">
      <h1>Login</h1>
      <div id="loginInputs">
        <input type="text" placeholder="Email" />
        <div id="passwordDiv">
          <input type="password" placeholder="Password" />
          <router-link class="link" to="/">Forgot Password?</router-link>
        </div>
        <button class="btn btn-blue">Login</button>
      </div>
      <div id="registerDiv">
        <button id="register">Not a member?</button>
        <router-link class="link" to="/register"> Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
#loginContainer {
  border-radius: 5px;
  color: black;
  padding: 25px;

  background-color: #eee;
}

#loginInputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 25px;
  margin-top: 25px;
}

#passwordDiv {
  display: flex;
  flex-direction: column;
}

h1 {
  color: black;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
}

input {
  border-radius: 5px;
  padding: 10px;
}

p {
  text-align: left;
}

#registerDiv {
  text-align: center;
}

#register {
  display: inline;
}

.link {
  color: #1e90ff;
}

.btn {
  @apply font-bold py-2 px-4 rounded;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
</style>
