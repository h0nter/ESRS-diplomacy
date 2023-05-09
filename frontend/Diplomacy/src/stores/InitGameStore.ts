import { computed, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";
import type { HostData } from "@/models/API_support";

export const API_URL = import.meta.env.VITE_HOST_URL + "/api";

export const useInitGameStore = defineStore("InitGameStore", () => {
  const hostRoom = ref<HostData>();
  const hostLoading = ref(false);
  const hostError = ref(false);
  const hostErrorM = ref("");

  const fetchHostRoom = async (host_id: Number, refresh: Boolean) => {
    // Check if the host room data is already loaded and if we are not refreshing
    if (hostRoom.value && !refresh) {
      return;
    }

    const host_config = {
      method: "get",
      url: API_URL + "/host/",
    };

    hostLoading.value = true;

    await axios(host_config)
      .then((response) => {
        // Get the room data from the response
        const allHosts: HostData[] = response.data;

        hostRoom.value = allHosts.find((host) => host.id === host_id);

        hostLoading.value = false;
      })
      .catch((err) => {
        hostError.value = true;
        hostErrorM.value = err;
        console.log(err);
        hostLoading.value = false;
      });
  };

  return {
    hostRoom,
    hostLoading,
    hostError,
    hostErrorM,
    fetchHostRoom,
  };
});
