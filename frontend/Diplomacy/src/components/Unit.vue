<template>
  <g :id="unitID">
    <use
      v-bind="{ 'xlink:href': '#' + type }"
      :style="'fill:' + color"
      :transform="
        'translate(' + (positionX + 8) + ', ' + (positionY - 14) + ')'
      "
      :class="'unit' + (mapStore.errorUnit === unitID ? ' error' : '')"
      @click="onUnitClick"
    />
    <UnitActionMenu
      v-show="mapStore.activeUnitName === unitID"
      :id="unitActionMenuID"
      :unit_id="unit_id"
      :type="type"
      :location_id="location_id"
      :location_name="location_name"
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
    unit_id: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
    location_id: {
      type: String,
      required: true,
    },
    location_name: {
      type: String,
      required: true,
    },
    locationIsSea: {
      type: Boolean,
      required: true,
    },
    locationIsCoast: {
      type: Boolean,
      required: true,
    },
    positionX: {
      type: Number,
      required: true,
    },
    positionY: {
      type: Number,
      required: true,
    },
  });

  const mapStore = useMapStore();
  const gameStore = useGameStore();

  const unitID = "unit-" + props.unit_id;
  const unitActionMenuID = unitID + "-menu";

  const onUnitClick = () => {
    // If no orders are set, show the action menu
    if (
      !mapStore.moveOrder &&
      !mapStore.supportOrder &&
      !mapStore.convoyOrder &&
      !mapStore.moveViaConvoyOrder
    ) {
      // Update the map state to show the action menu
      mapStore.unitClickHandler(unitID, unitActionMenuID);
      // Update the game state to the active unit
      gameStore.activeUnitID = parseInt(props.unit_id!);
      gameStore.currentLocationID = parseInt(props.location_id!);
    }

    // If it's support order, add this unit and territory as reference
    if (
      mapStore.supportOrder &&
      gameStore.activeUnitID !== parseInt(props.unit_id)
    ) {
      mapStore.supportHandler(
        props.location_id,
        props.location_name,
        false,
        props.unit_id
      );
    }

    // If it's a convoy order, add this unit and territory as reference
    if (
      mapStore.convoyOrder &&
      gameStore.activeUnitID !== parseInt(props.unit_id)
    ) {
      mapStore.supportHandler(
        props.location_id,
        props.location_name,
        false,
        props.unit_id
      );
    }
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

  .error {
    stroke: hsl(5, 100%, 65%);
    stroke-width: 3px;
  }

  .action-menu {
    display: none;
  }

  .action-menu.active {
    display: block !important;
  }
</style>
