<template>
  <div class="h-full w-full flex justify-center items-center">
    <div id="loginContainer">
      <h1>Register</h1>
      <div id="loginInputs">
        <input type="text" placeholder="Email" />
        <input type="text" placeholder="Username" />
        <div id="passwordDiv">
          <input type="password" placeholder="Password" />
        </div>
        <div id="passwordDiv2">
          <input type="password" placeholder="Re-enter Password" />
        </div>
        <button class="btn btn-blue">Register</button>
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
  margin-top: 25px;
}

#passwordDiv,
#passwordDiv2 {
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
