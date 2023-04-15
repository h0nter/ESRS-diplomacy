<template>
  <use v-bind="{'xlink:href' : '#' + type}" :id="'unit-'+unit_id" :style="'fill:' + color" :transform="'translate(' + (positionX + 8) + ', ' + (positionY - 14) + ')'" class="unit" @click="onUnitClick"/>
  <UnitActionMenu :unit_id="unit_id" :type="type" :positionX="positionX + 8" :positionY="positionY - 14" v-bind:class="[actionMenuOpen ? 'action-menu active' : 'action-menu']"/>
</template>

<script lang="ts" setup>
import {defineProps, PropType} from "vue";
import UnitActionMenu from "@/components/UnitActionMenu.vue";

const props = defineProps({
  unit_id: String,
  type: String,
  color: String,
  positionX: Number,
  positionY: Number,
});

let actionMenuOpen : Boolean = false;
const onUnitClick = () => {
  // Toggle the action menu
  console.log(`Unit $unit_id clicked`)
  actionMenuOpen = !actionMenuOpen;
}
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