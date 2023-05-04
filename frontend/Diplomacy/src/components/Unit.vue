<template>
  <g :id="unitID">
    <use
      v-bind="{ 'xlink:href': '#' + type }"
      :style="'fill:' + color"
      :transform="
        'translate(' + (positionX + 8) + ', ' + (positionY - 14) + ')'
      "
      class="unit"
      @click="onUnitClick"
    />
    <UnitActionMenu
      v-show="mapStore.activeUnitName === unitID"
      :id="unitActionMenuID"
      :unit_id="unit_id"
      :type="type"
      :location_id="location_id"
      :locationIsSea="locationIsSea"
      :locationIsCoast="locationIsCoast"
      :positionX="positionX + 8"
      :positionY="positionY - 14"
    />
  </g>
</template>

<script lang="ts" setup>
  import { defineProps, PropType } from "vue";
  import UnitActionMenu from "@/components/UnitActionMenu.vue";
  import { useMapStore } from "@/stores/MapStore";
  import { useGameStore } from "@/stores/GameStore";

  const props = defineProps({
    unit_id: String,
    type: String,
    color: String,
    location_id: String,
    locationIsSea: Boolean,
    locationIsCoast: Boolean,
    positionX: Number,
    positionY: Number,
  });

  const mapStore = useMapStore();
  const gameStore = useGameStore();

  const unitID = "unit-" + props.unit_id;
  const unitActionMenuID = unitID + "-menu";

  const onUnitClick = () => {
    // Update the map state to show the action menu
    mapStore.unitClickHandler(unitID, unitActionMenuID);
    // Update the game state to the active unit
    gameStore.setActiveUnitID(parseInt(props.unit_id!));
    gameStore.setCurrentLocationID(parseInt(props.location_id!));
  };
</script>

<style scoped>
  .unit {
    stroke: black;
    stroke-width: 1px;
  }

  .unit:hover {
    stroke-width: 2px;
  }

  .action-menu {
    display: none;
  }

  .action-menu.active {
    display: block !important;
  }
</style>
