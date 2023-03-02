<template>
<g :title="territory">
  <use v-bind="{'xlink:href' : '#' + type}" :id="territory" :class="country" :transform="'translate(' + (positionX + 8) + ', ' + (positionY - 14) + ')'"/>
</g>
</template>

<script setup>
import {Country} from "@/models/Country";

const props = defineProps({
  type: ('A'|'F'|'sc'),
  territory: String,
  country: Country,
  positionX: Number,
  positionY: Number,
});
</script>

<style scoped>
@import "@/assets/countries.css";

 g:hover{
      @apply active
 }

 .active {
        stroke-width: 3px;
    }
</style>