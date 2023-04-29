<template>
  <div class="flex-col justify-center items-center">
    <p v-if="init_error" class="text-red-600">
      Something went wrong: {{ init_error }}
    </p>
    <p v-if="init_loading">
      Loading...
    </p>
    <svg v-else viewBox="-0.5 -0.5 610 560" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <UnitsSetup />
      <UnitActonMenuSetup/>
      <Territory v-for="territory in territories" :key="territory.id" :name="territory.name" :polygons="territory.polygons" :text="territory.abbreviation" :textX="territory.textPosX" :textY="territory.textPosY" :units="units" @territoryHovered="onTerritoryHovered" />
      <use id="territoryOnTop" :href="currentlyHoveredTerritory" />
      <Unit v-for="unit in units" :key="unit.id" :unit_id="unit.id" :type="[unit.canFloat ? 'F' : 'A']" :color="unit.owner.colour" :positionX="unit.location.textPosX" :positionY="unit.location.textPosY" :activeUnit="activeUnitName" @unitClicked="onUnitClick"/>
      <use id="activeUnit" :href="activeUnit" />
      <use id="activeUnitMenu" :href="activeUnitMenu" />
    </svg>
  </div>
</template>

<script lang="ts" setup>
  import { INITIAL_MAP_SETUP } from "@/gql/documents/map";
  import {useQuery} from '@vue/apollo-composable'
  import {computed, watchEffect} from 'vue'


  import { ref } from 'vue'
  import Territory from "@/components/Territory.vue";
  import Unit from "@/components/Unit.vue";
  import UnitsSetup from "@/components/UnitsSetup.vue";
  import type {LocationType, UnitType} from "@/gql/graphql";
  import UnitActonMenuSetup from "@/components/UnitActonMenuSetup.vue";
  import UnitActionMenu from "@/components/UnitActionMenu.vue";

  const currentlyHoveredTerritory = ref("#");

  const activeUnit = ref("#");
  const activeUnitMenu = ref("#");
  let activeUnitName : string = "";

  function onTerritoryHovered(name:string) {
    currentlyHoveredTerritory.value = "#" + name;
  }

  // TODO: Create a type for those args, cause it's also defined in Unit.vue
  const onUnitClick = (args : {unit_id:string,unit_menu_id:string}) => {
    if (args.unit_id === activeUnitName) {
      activeUnitName = "#";
    }else{
      activeUnitName = args.unit_id;
    }
    activeUnit.value = "#" + args.unit_id;
    activeUnit.value = "#";
    activeUnitMenu.value = "#" + args.unit_menu_id;
  }

  const {result : init_return, loading : init_loading, error : init_error} = useQuery(INITIAL_MAP_SETUP);

  let territories : LocationType[] = [];
  let units : UnitType[] = [];

  watchEffect(() => {
    territories = (computed(() => init_return.value?.locations).value);
    units = (computed(() => init_return.value?.units).value);
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