<template>
  <line
    v-if="
      (orderType !== RoomOrderInstructionChoices.Hld &&
        targetLocation !== null) ||
      (orderType === RoomOrderInstructionChoices.Spt &&
        referenceTargetLocation !== null)
    "
    :x1="currentLocation.textPosX"
    :y1="currentLocation.textPosY"
    :x2="target.X"
    :y2="target.Y"
    :stroke="dashed ? 'rgba(0, 0, 0, 40%)' : 'rgba(0, 0, 0, 100%)'"
    stroke-width="2"
    :stroke-dasharray="dashed ? '10,3' : ''"
    :marker-end="dashed ? '' : 'url(#arrowhead-bold)'"
  />
  <line
    v-if="orderType === RoomOrderInstructionChoices.Spt"
    :x1="referenceCurrentLocation.textPosX"
    :y1="referenceCurrentLocation.textPosY"
    :x2="referenceTargetLocation.textPosX"
    :y2="referenceTargetLocation.textPosY"
    stroke="rgba(0, 0, 0, 40%)"
    stroke-width="2"
    marker-end="url(#arrowhead-light)"
  />
</template>

<script setup lang="ts">
  import type { LocationType } from "@/gql/graphql";
  import { RoomOrderInstructionChoices } from "@/gql/graphql";
  import { computed, ComputedRef } from "vue";
  import type { Vector2D } from "@/models/Vector2D";

  const props = defineProps<{
    currentLocation: LocationType;
    targetLocation: LocationType | null;
    referenceCurrentLocation: LocationType | null;
    referenceTargetLocation: LocationType | null;
    orderType: RoomOrderInstructionChoices;
  }>();

  let dashed = computed(() => {
    return (
      props.orderType === RoomOrderInstructionChoices.Spt ||
      props.orderType === RoomOrderInstructionChoices.Cvy
    );
  });

  const target: ComputedRef<Vector2D> = computed(() => {
    if (
      props.targetLocation === null &&
      props.referenceTargetLocation !== null &&
      props.referenceCurrentLocation !== null
    ) {
      // Calculate halfway point of the vector between the two reference locations
      const x =
        props.referenceCurrentLocation.textPosX +
        (props.referenceTargetLocation.textPosX -
          props.referenceCurrentLocation.textPosX) /
          2;

      const y =
        props.referenceCurrentLocation.textPosY +
        (props.referenceTargetLocation.textPosY -
          props.referenceCurrentLocation.textPosY) /
          2;

      return { X: x, Y: y };
    } else if (props.targetLocation !== null) {
      return {
        X: props.targetLocation.textPosX,
        Y: props.targetLocation.textPosY,
      };
    } else {
      return { X: 0, Y: 0 };
    }
  });
</script>

<style scoped></style>
