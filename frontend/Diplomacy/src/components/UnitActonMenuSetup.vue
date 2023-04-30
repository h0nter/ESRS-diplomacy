<template>
  <g id="HoldButton">
    <rect width="44" height="26" ry="12" rx="12" />
    <text x="22" y="14">Hold</text>
  </g>
  <g id="SupportButton">
    <rect width="60" height="26" ry="12" rx="12" />
    <text x="30" y="14">Support</text>
  </g>
  <g id="MoveButton">
    <rect width="44" height="26" ry="12" rx="12" />
    <text x="22" y="14">Move</text>
  </g>
  <g id="ConvoyButton">
    <rect width="54" height="26" ry="12" rx="12" />
    <text x="27" y="14">Convoy</text>
  </g>
</template>

<script setup lang="ts">
  const props = defineProps<{}>();
</script>

<style scoped>
  rect {
    fill: white;
    filter: drop-shadow(0 0.2rem 0.2rem rgba(0, 0, 0, 0.5));
  }

  text {
    font-size: 10px;
    text-anchor: middle;
    dominant-baseline: middle;
  }
</style>
