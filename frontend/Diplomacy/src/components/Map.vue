<template>
  <div class="flex-col justify-center items-center">
    <p v-if="init_error" class="text-red-600">
      Something went wrong: {{ init_error }}
    </p>
    <p v-if="init_loading">Loading...</p>
    <svg
      v-else
      viewBox="-0.5 -0.5 610 560"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
    >
      <!-- Instantiate a single unit and action menu, then 'use' tag will clone them -->
      <UnitsSetup />
      <UnitActonMenuSetup />
      <!-- Create territories, and use-tag for hover mechanics -->
      <Territory
        v-for="territory in territories"
        :key="territory.id"
        :name="territory.name"
        :countryColor="territory.currentOwner?.colour"
        :polygons="territory.polygons"
        :text="territory.abbreviation"
        :textX="territory.textPosX"
        :textY="territory.textPosY"
      />
      <use id="territoryOnTop" :href="mapStore.territoryHovered" />
      <!-- Create units, and use-tag for click mechanics -->
      <Unit
        v-for="unit in units"
        :key="unit.id"
        :unit_id="unit.id"
        :type="unit.canFloat ? 'F' : 'A'"
        :color="unit.owner.colour"
        :location_name="unit.location.name"
        :location_id="unit.location.id"
        :locationIsSea="unit.location.isSea"
        :locationIsCoast="unit.location.isCoast"
        :positionX="unit.location.textPosX"
        :positionY="unit.location.textPosY"
      />
      <use id="activeUnit" :href="mapStore.activeUnit" />
      <!-- Ensure that the active menu is rendered in front of units and territories -->
      <use id="activeUnitMenu" :href="mapStore.activeUnitMenu" />
    </svg>
  </div>
</template>

<script lang="ts" setup>
  import {
    INITIAL_MAP_SETUP,
    PLAYER_ORDERS,
    TURNS,
    UPDATE_ORDER,
  } from "@/gql/documents/map";
  import { useQuery, useLazyQuery, useMutation } from "@vue/apollo-composable";
  import { computed, watchEffect } from "vue";

  import { ref } from "vue";
  import Territory from "@/components/Territory.vue";
  import Unit from "@/components/Unit.vue";
  import UnitsSetup from "@/components/UnitsSetup.vue";
  import type {
    LocationType,
    OrderType,
    TurnType,
    UnitType,
  } from "@/gql/graphql";
  import UnitActonMenuSetup from "@/components/UnitActonMenuSetup.vue";
  import { RoomOrderInstructionChoices } from "@/gql/graphql";
  import { useMapStore } from "@/stores/MapStore";
  import { useGameStore } from "@/stores/GameStore";

  // Load store for handling territory hover and unit clicks
  const mapStore = useMapStore();
  const gameStore = useGameStore();

  gameStore.turnStart();

  const {
    result: init_return,
    loading: init_loading,
    error: init_error,
  } = useQuery(INITIAL_MAP_SETUP);

  let territories: LocationType[] = [];
  let units: UnitType[] = [];

  watchEffect(() => {
    territories = computed(() => init_return.value?.locations).value;
    units = computed(() => init_return.value?.units).value;
  });
</script>

<style scoped>
  div {
    align-items: center;
    display: flex;
    justify-content: center;
    width: 90%;
  }

  svg {
    border: 1.25px solid black;
    max-height: 100vh;
    max-width: 100vw;
    width: 100%;
    stroke-width: 0.75px;
  }

  #territoryOnTop:hover {
    stroke-width: 2.5px;
  }
</style>
