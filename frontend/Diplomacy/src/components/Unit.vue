<template>
<use v-bind="{'xlink:href' : '#' + type}" :id="'unit-'+unit_id" :style="'fill:' + color" :transform="'translate(' + (positionX + 8) + ', ' + (positionY - 14) + ')'" class="unit"/>
</template>

<script setup>
import {Country} from "@/models/Country";

const props = defineProps({
  unit_id: String,
  type: ('A'|'F'),
  color: String,
  positionX: Number,
  positionY: Number,
});
</script>

<style scoped>
  .unit {
    stroke: black;
    stroke-width: 1px;
  }
</style>