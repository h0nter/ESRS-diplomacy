<template>
  <line
    v-if="
      orderType !== RoomOrderInstructionChoices.Hld && targetLocation !== null
    "
    :x1="currentLocation.textPosX"
    :y1="currentLocation.textPosY"
    :x2="targetLocation.textPosX"
    :y2="targetLocation.textPosY"
    :stroke="dashed ? 'rgba(0, 0, 0, 40%)' : 'rgba(0, 0, 0, 100%)'"
    stroke-width="3"
    :stroke-dasharray="dashed ? '10,10' : ''"
    marker-end="url(#arrowhead)"
  />
</template>

<script setup lang="ts">
  import type { LocationType } from "@/gql/graphql";
  import { RoomOrderInstructionChoices } from "@/gql/graphql";
  import { computed } from "vue";

  const props = defineProps<{
    currentLocation: LocationType;
    targetLocation: LocationType | null;
    orderType: RoomOrderInstructionChoices;
  }>();

  let dashed = computed(() => {
    return (
      props.orderType === RoomOrderInstructionChoices.Spt ||
      props.orderType === RoomOrderInstructionChoices.Cvy
    );
  });
</script>

<style scoped></style>
