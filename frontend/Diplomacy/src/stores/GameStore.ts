import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useApolloClient } from "@vue/apollo-composable";
import { PLAYER_ORDERS, TURNS, UPDATE_ORDER } from "@/gql/documents/map";
import type { OrderType, TurnType } from "@/gql/graphql";
import { RoomOrderInstructionChoices } from "@/gql/graphql";

export const useGameStore = defineStore("GameStore", () => {
  const { resolveClient } = useApolloClient();
  const client = resolveClient();

  const activeUnitID = ref<number>(0);
  const currentLocationID = ref<number>(0);
  const turns = ref<TurnType[]>([]);
  const orders = ref<OrderType[]>([]);

  const turnStart = async () => {
    const turns_result = await client.query({ query: TURNS });
    turns.value = computed(() => turns_result.data?.turns ?? []).value;

    const orders_result = await client.query({ query: PLAYER_ORDERS });
    orders.value = computed(() => orders_result.data?.orders ?? []).value;
  };

  const setActiveUnitID = (unitID: number) => {
    activeUnitID.value = unitID;
  };

  const setCurrentLocationID = (locationID: number) => {
    currentLocationID.value = locationID;
  };

  const holdHandler = async () => {
    // Get orders only for the active unit and the current turn
    const currOrderID = orders.value.find(
      (o) =>
        parseInt(o.targetUnit!.id) === activeUnitID.value &&
        o.turn!.id === turns.value[0].id
    )?.id;

    const order_update_result = await client.mutate({
      mutation: UPDATE_ORDER,
      variables: {
        unitID: activeUnitID.value,
        instruction: RoomOrderInstructionChoices.Hld,
        turnID: parseInt(turns.value[0].id),
        currentLocation: currentLocationID.value,
        orderID: currOrderID,
      },
    });
    console.log(order_update_result.data);
  };

  return {
    activeUnitID,
    currentLocationID,
    setActiveUnitID,
    setCurrentLocationID,
    holdHandler,
    turnStart,
  };
});
