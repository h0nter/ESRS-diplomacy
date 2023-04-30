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
        :polygons="territory.polygons"
        :text="territory.abbreviation"
        :textX="territory.textPosX"
        :textY="territory.textPosY"
        :units="units"
        @territoryHovered="onTerritoryHovered"
      />
      <use id="territoryOnTop" :href="currentlyHoveredTerritory" />
      <!-- Create units, and use-tag for click mechanics -->
      <Unit
        v-for="unit in units"
        :key="unit.id"
        :unit_id="unit.id"
        :type="[unit.canFloat ? 'F' : 'A']"
        :color="unit.owner.colour"
        :positionX="unit.location.textPosX"
        :positionY="unit.location.textPosY"
        :activeUnit="activeUnitName"
        @unitClicked="onUnitClick"
      />
      <use id="activeUnit" :href="activeUnit" />
      <!-- Ensure that the active menu is rendered in front of units and territories -->
      <use id="activeUnitMenu" :href="activeUnitMenu" />
    </svg>
  </div>
</template>

<script lang="ts" setup>
  import { INITIAL_MAP_SETUP } from "@/gql/documents/map";
  import { useQuery } from "@vue/apollo-composable";
  import { computed, watchEffect } from "vue";

  import { ref } from "vue";
  import Territory from "@/components/Territory.vue";
  import Unit from "@/components/Unit.vue";
  import UnitsSetup from "@/components/UnitsSetup.vue";
  import type { LocationType, UnitType } from "@/gql/graphql";
  import UnitActonMenuSetup from "@/components/UnitActonMenuSetup.vue";
  import UnitActionMenu from "@/components/UnitActionMenu.vue";
  import type { UnitClickObject } from "@/models/UnitClickObject";

  const currentlyHoveredTerritory = ref("#");

  function onTerritoryHovered(name: string) {
    currentlyHoveredTerritory.value = "#" + name;
  }

  // Begin active unit and action menu logic

  // Set up the refs and name vars,
  // why not set them up together in an object? Because it doesn't work.
  const activeUnit = ref("#");
  const activeUnitMenu = ref("#");
  let activeUnitName: string = "";

  /*
   * Triggered by the Unit component when a unit is clicked.
   * Update the state of the active unit and menu, pass the state to all units to toggle the menu on/off.
   * It has to be done outside the Unit component, to order the rendering of those correctly.
   */
  const onUnitClick = (args: UnitClickObject) => {
    // If the active unit is clicked again, close the menu
    if (args.unit_id === activeUnitName) {
      activeUnitName = "#";
    } else {
      // Otherwise, open the menu (only one open at a time)
      activeUnitName = args.unit_id;
    }
    // This here is a stupid hack to force the re-rendering/drawing of the active unit and menu.
    activeUnit.value = "#" + args.unit_id;
    activeUnit.value = "#";
    activeUnitMenu.value = "#" + args.unit_menu_id;
  };

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
