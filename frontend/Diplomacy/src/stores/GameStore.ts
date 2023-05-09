import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { provideApolloClient, useApolloClient } from "@vue/apollo-composable";
import { PLAYER_ORDERS, TURNS, UPDATE_ORDER } from "@/gql/documents/map";
import type { OrderType, TurnType } from "@/gql/graphql";
import { RoomOrderInstructionChoices } from "@/gql/graphql";
import type { MutationOptions } from "@apollo/client";
import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client/core";

export const useGameStore = defineStore("GameStore", () => {
  const { resolveClient } = useApolloClient();
  const client = resolveClient();

  const roomID = ref<number>(0);
  const turnID = ref<number>(0);
  const activePlayerID = ref<string>("0");

  const activeUnitID = ref<number>(0);
  const currentLocationID = ref<number>(0);
  const targetLocationID = ref<number>(0);

  const referenceUnitID = ref<number>(0);
  const referenceUnitCurrentLocationID = ref<number>(0);
  const referenceUnitTargetLocationID = ref<number>(0);

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
    const currOrderResponse = await client.query({
      query: PLAYER_ORDERS,
      variables: () => {
        return {
          roomID: roomID.value,
          unitID: activeUnitID.value,
          turnID: parseInt(turns.value[0].id),
        };
      },
    });

    const currOrderID = parseInt(currOrderResponse.data?.order[0].id);

    console.log(currOrderID);

    let options: MutationOptions | null = null;

    if (instruction === RoomOrderInstructionChoices.Hld) {
      options = {
        mutation: UPDATE_ORDER,
        variables: {
          roomID: roomID.value,
          unitID: activeUnitID.value,
          instruction: instruction,
          turnID: turnID.value,
          currentLocation: currentLocationID.value,
        },
      };
    } else if (
      instruction === RoomOrderInstructionChoices.Spt ||
      instruction === RoomOrderInstructionChoices.Cvy
    ) {
      options = {
        mutation: UPDATE_ORDER,
        variables: {
          roomID: roomID.value,
          unitID: activeUnitID.value,
          instruction: instruction,
          turnID: turnID.value,
          currentLocation: currentLocationID.value,
          referenceUnitID: referenceUnitID.value,
          referenceUnitCurrentLocation: referenceUnitCurrentLocationID.value,
          referenceUnitTargetLocation: referenceUnitTargetLocationID.value,
        },
      };
    } else {
      options = {
        mutation: UPDATE_ORDER,
        variables: {
          roomID: roomID.value,
          unitID: activeUnitID.value,
          instruction: instruction,
          turnID: turnID.value,
          currentLocation: currentLocationID.value,
          targetLocation: targetLocationID.value,
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
      const ordersCopy = [...orders.value];
      ordersCopy[orderIndex] = order;
      orders.value = ordersCopy;
    }

    // Reset the state for next order
    activeUnitID.value = 0;
    currentLocationID.value = 0;
    targetLocationID.value = 0;
    referenceUnitID.value = 0;
    referenceUnitCurrentLocationID.value = 0;
    referenceUnitTargetLocationID.value = 0;

    console.log("order ok? " + order_update_result.data.updateOrder.ok);

    return order_update_result.data.updateOrder.ok;
  };

  const setNewGraphQLLink = (url: string) => {
    const httpLink = new HttpLink({
      uri: url,
    });

    client.setLink(httpLink);
  };

  return {
    roomID,
    activePlayerID,
    turnID,
    orders,
    activeUnitID,
    currentLocationID,
    targetLocationID,
    referenceUnitID,
    referenceUnitCurrentLocationID,
    referenceUnitTargetLocationID,
    setActiveUnitID,
    setCurrentLocationID,
    updateOrder,
    turnStart,
    setNewGraphQLLink,
  };
});
