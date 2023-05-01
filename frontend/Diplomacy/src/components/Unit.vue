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
      v-show="activeUnit === unitID"
      :id="unitActionMenuID"
      :unit_id="unit_id"
      :type="type"
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
  import type { UnitClickObject } from "@/models/UnitClickObject";

  const props = defineProps({
    unit_id: String,
    type: String,
    color: String,
    locationIsSea: Boolean,
    locationIsCoast: Boolean,
    positionX: Number,
    positionY: Number,
    activeUnit: String,
  });

  const emit = defineEmits(["unitClicked"]);

  const unitID = "unit-" + props.unit_id;
  const unitActionMenuID = unitID + "-menu";

  const onUnitClick = () => {
    // Toggle the action menu
    emit("unitClicked", <UnitClickObject>{
      unit_id: unitID,
      unit_menu_id: unitActionMenuID,
    });
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
