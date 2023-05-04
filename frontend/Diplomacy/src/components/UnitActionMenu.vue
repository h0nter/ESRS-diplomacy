<template>
  <g>
    <use
      v-bind="{ 'xlink:href': '#HoldButton' }"
      :id="'hold-' + unit_id"
      :transform="
        'translate(' + (positionX - 68) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
      @click="mapStore.holdHandler()"
    />
    <use
      v-bind="{ 'xlink:href': '#SupportButton' }"
      :id="'support-' + unit_id"
      :transform="
        'translate(' + (positionX - 30) + ', ' + (positionY - 50) + ')'
      "
      class="action-button"
      @click="mapStore.supportHandler(location_name)"
    />
    <use
      v-bind="{ 'xlink:href': '#MoveButton' }"
      :id="'move-' + unit_id"
      :transform="
        'translate(' + (positionX + 25) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
      @click="mapStore.moveHandler(location_name)"
    />
    <use
      v-if="type === 'F' && locationIsSea"
      v-bind="{ 'xlink:href': '#ConvoyButton' }"
      :id="'convoy-' + unit_id"
      :transform="
        'translate(' + (positionX - 28) + ', ' + (positionY + 20) + ')'
      "
      class="action-button"
      @click="mapStore.convoyHandler(location_name)"
    />
    <use
      v-if="type === 'A' && locationIsCoast"
      v-bind="{ 'xlink:href': '#ViaConvoyButton' }"
      :id="'via-convoy-' + unit_id"
      :transform="
        'translate(' + (positionX - 30) + ', ' + (positionY + 20) + ')'
      "
      class="action-button"
      @click="mapStore.moveViaConvoyHandler(location_name)"
    />
  </g>
</template>

<script lang="ts" setup>
  import { useMapStore } from "@/stores/MapStore";

  const props = defineProps({
    unit_id: String,
    type: String,
    location_id: String,
    location_name: String,
    locationIsSea: Boolean,
    locationIsCoast: Boolean,
    positionX: Number,
    positionY: Number,
  });

  const mapStore = useMapStore();
</script>

<style scoped>
  .action-button {
    cursor: pointer;
  }

  .action-button:hover {
    stroke-width: 2px;
  }
</style>
