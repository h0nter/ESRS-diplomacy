<template>
  <g>
    <use
      v-bind="{ 'xlink:href': '#HoldButton' }"
      :id="'hold-' + unit_id"
      :transform="
        'translate(' + (positionX - 68) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
    />
    <use
      v-bind="{ 'xlink:href': '#SupportButton' }"
      :id="'support-' + unit_id"
      :transform="
        'translate(' + (positionX - 30) + ', ' + (positionY - 50) + ')'
      "
      class="action-button"
    />
    <use
      v-bind="{ 'xlink:href': '#MoveButton' }"
      :id="'move-' + unit_id"
      :transform="
        'translate(' + (positionX + 25) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
    />
    <!-- TODO: Conditional rendering of convoy button based on unit location -->
    <use
      v-if="type == 'F'"
      v-bind="{ 'xlink:href': '#ConvoyButton' }"
      :id="'convoy-' + unit_id"
      :transform="
        'translate(' + (positionX - 28) + ', ' + (positionY + 20) + ')'
      "
      class="action-button"
    />
  </g>
</template>

<script lang="ts" setup>
  import type { PropType } from "vue";

  const props = defineProps({
    unit_id: String,
    type: String,
    positionX: Number,
    positionY: Number,
  });
</script>

<style scoped></style>
