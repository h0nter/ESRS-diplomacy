import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("AuthStore", () => {
  const token = ref<string | null>(null);
  const userID = ref<string | null>(null);

  const login = async (username: string, password: string) => {
    let data = new FormData();
    data.append("username", username);
    data.append("password", password);

    let config = {
      method: "post",
      url: "http://127.0.0.1:8000/api/get_login/",
      data: data,
    };

    const response = await axios(config);

    if (response.data === "not authenticated") {
      let error = new Error("Not authenticated");
      throw error;
    }

    localStorage.setItem("token", response.data.user_id);
    localStorage.setItem("userID", response.data.user_id);

    token.value = response.data.user_id;
    userID.value = response.data.user_id;
  };

  const register = async (
    email: string,
    username: string,
    password: string
  ) => {
    let data = new FormData();
    data.append("email", email);
    data.append("username", username);
    data.append("password", password);
    data.append("first_name", "");
    data.append("last_name", "");

    let config = {
      method: "post",
      url: "http://127.0.0.1:8000/api/register/",
      data: data,
    };

    let response;

    try {
      response = await axios(config);
    } catch (error) {
      let errors = JSON.parse(error.request.response);
      let errorString = "";
      for (let key in errors) {
        errorString += key + ": " + errors[key] + "<br>";
        console.log(errorString);
      }
      throw errorString;
    }

    console.log(response);

    localStorage.setItem("token", response.data.id);
    localStorage.setItem("userID", response.data.id);

    token.value = response.data.id;
    userID.value = response.data.id;
  };

  const logout = async () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userID");

    token.value = null;
    userID.value = null;
  };

  const tryLogin = async () => {
    const myToken = localStorage.getItem("token");
    const myUserID = localStorage.getItem("userID");

    if (myToken && myUserID) {
      token.value = myToken;
      userID.value = myUserID;
    }
  };

  return {
    token,
    userID,
    login,
    register,
    logout,
    tryLogin,
  };
});
