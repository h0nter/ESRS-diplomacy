import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useApolloClient } from "@vue/apollo-composable";
import { PLAYER_ORDERS, TURNS, UPDATE_ORDER } from "@/gql/documents/map";
import type { OrderType, TurnType } from "@/gql/graphql";
import { RoomOrderInstructionChoices } from "@/gql/graphql";
import type { MutationOptions } from "@apollo/client";

export const useGameStore = defineStore("GameStore", () => {
  const { resolveClient } = useApolloClient();
  const client = resolveClient();

  const activeUnitID = ref<number>(0);
  const currentLocationID = ref<number>(0);
  const targetLocationID = ref<number>(0);
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

  const updateOrder = async (instruction: RoomOrderInstructionChoices) => {
    // Get the order id for the current unit and turn
    const currOrderID = orders.value.find(
      (o) =>
        parseInt(o.targetUnit!.id) === activeUnitID.value &&
        o.turn!.id === turns.value[0].id
    )?.id;

    let options: MutationOptions | null = null;

    if (instruction === RoomOrderInstructionChoices.Hld) {
      options = {
        mutation: UPDATE_ORDER,
        variables: {
          unitID: activeUnitID.value,
          instruction: instruction,
          turnID: parseInt(turns.value[0].id),
          currentLocation: currentLocationID.value,
          orderID: currOrderID,
        },
      };
    } else {
      options = {
        mutation: UPDATE_ORDER,
        variables: {
          unitID: activeUnitID.value,
          instruction: instruction,
          turnID: parseInt(turns.value[0].id),
          currentLocation: currentLocationID.value,
          targetLocation: targetLocationID.value,
          orderID: currOrderID,
        },
      };
    }
    const order_update_result = await client.mutate(options);

    // Check if the update was successful
    if (order_update_result.data.updateOrder.ok) {
      // Update the order in the state
      const order: OrderType = order_update_result.data.updateOrder.order;
      const orderIndex: number = orders.value.findIndex(
        (o) => o.id === order.id
      );
      console.log(order);
      const ordersCopy = [...orders.value];
      ordersCopy[orderIndex] = order;
      orders.value = ordersCopy;
    }
  };

  return {
    orders,
    activeUnitID,
    currentLocationID,
    targetLocationID,
    setActiveUnitID,
    setCurrentLocationID,
    updateOrder,
    turnStart,
  };
});
