<template>
  <g>
    <use
      v-bind="{ 'xlink:href': '#HoldButton' }"
      :id="'hold-' + unit_id"
      :transform="
        'translate(' + (positionX - 68) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
      @click="actionClickedDispatcher(RoomOrderInstructionChoices.Hld)"
    />
    <use
      v-bind="{ 'xlink:href': '#SupportButton' }"
      :id="'support-' + unit_id"
      :transform="
        'translate(' + (positionX - 30) + ', ' + (positionY - 50) + ')'
      "
      class="action-button"
      @click="actionClickedDispatcher(RoomOrderInstructionChoices.Hld)"
    />
    <use
      v-bind="{ 'xlink:href': '#MoveButton' }"
      :id="'move-' + unit_id"
      :transform="
        'translate(' + (positionX + 25) + ', ' + (positionY - 15) + ')'
      "
      class="action-button"
      @click="actionClickedDispatcher(RoomOrderInstructionChoices.Hld)"
    />
    <use
      v-if="type === 'F' && locationIsSea"
      v-bind="{ 'xlink:href': '#ConvoyButton' }"
      :id="'convoy-' + unit_id"
      :transform="
        'translate(' + (positionX - 28) + ', ' + (positionY + 20) + ')'
      "
      class="action-button"
      @click="actionClickedDispatcher(RoomOrderInstructionChoices.Hld)"
    />
    <use
      v-if="type === 'A' && locationIsCoast"
      v-bind="{ 'xlink:href': '#ViaConvoyButton' }"
      :id="'via-convoy-' + unit_id"
      :transform="
        'translate(' + (positionX - 30) + ', ' + (positionY + 20) + ')'
      "
      class="action-button"
      @click="actionClickedDispatcher('VCV')"
    />
  </g>
</template>

<script lang="ts" setup>
import type { ActionClickObject, ExtOrderInstructionChoices } from "@/models/ActionClickObject";
  import { RoomOrderInstructionChoices } from "@/gql/graphql";

  const props = defineProps({
    unit_id: String,
    type: String,
    locationIsSea: Boolean,
    locationIsCoast: Boolean,
    positionX: Number,
    positionY: Number,
  });

  const emit = defineEmits(["actionClicked"]);

  // Dispatch the action type + unitID to the map component
  const actionClickedDispatcher = (action: ExtOrderInstructionChoices) => {
    emit("actionClicked", <ActionClickObject><unknown>{
      unitID: props.unit_id,
      actionType: action
    });
  };
</script>

<style scoped>
  .action-button {
    cursor: pointer;
  }

  .action-button:hover {
    stroke-width: 2px;
  }
</style>
