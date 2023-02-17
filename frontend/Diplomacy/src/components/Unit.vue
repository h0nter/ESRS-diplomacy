<template>
<g :class="type">
  <path v-if="type === 'A'" d="M9,-6 L2,0 M9,6 L0,0"/>
	<path v-if="type === 'A'" d="M-11,-6 v4 h17 a2,2 0,0 0 0,-4z"/>
	<circle v-if="type === 'A'" r="6"/>
  <polygon v-if="type === 'F'" points="-2,-3 10,-3 -2,-13"/>
	<polygon v-if="type === 'F'" points="-12,-1 -6,5 6,5 12,-1"/>
  <circle v-if="type === 'sc'" r="4"/>
</g>
</template>

<script setup>
const props = defineProps({
  type: String,
});
</script>

<style scoped>
 g:hover{
      @apply active
 }

 .active {
        stroke-width: 3px;
    }
</style>