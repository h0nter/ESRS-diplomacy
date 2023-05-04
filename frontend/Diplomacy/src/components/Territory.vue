<template>
  <g
    :title="name"
    :id="'territory-' + name"
    :coast="isCoast"
    :class="isActive ? 'active' : ''"
    @mouseenter="mapStore.territoryHoverHandler(name)"
  >
    <polygon
      v-for="polygon in polygons"
      :key="polygon.id"
      :class="[polygon.colour === PolygonColourChoices.Land ? 'l' : 'w']"
      :points="polygon.polygon"
      :style="
        polygon.colour !== PolygonColourChoices.Aqua ? 'fill:' + fillColour : ''
      "
    />
    <text :x="textX" :y="textY">{{ text }}</text>
  </g>

  <!--  v-bind="{'xlink:href' : unit}"-->
</template>

<script lang="ts" setup>
  import { PropType, ref, Ref, watch, watchEffect } from "vue";
  import type { Map_PolygonType, UnitType } from "@/gql/graphql";
  import { RoomMap_PolygonColourChoices } from "@/gql/graphql";
  import { useMapStore } from "@/stores/MapStore";
  import { ColorTranslator, HSLObject } from "colortranslator";
  import { storeToRefs } from "pinia";

  const props = defineProps({
    name: String,
    countryColor: String,
    polygons: Array as PropType<Map_PolygonType[]>,
    isCoast: Boolean,
    text: String,
    textX: Number,
    textY: Number,
  });

  const isActive = ref<boolean>(false);

  const mapStore = useMapStore();

  const { currentTerritory } = storeToRefs(mapStore);

  const PolygonColourChoices: any = RoomMap_PolygonColourChoices;

  const colourTints = ref<string[]>(ColorTranslator.getTints("#ffffdd", 3));
  const fillColour = ref<string>(
    colourTints.value[colourTints.value.length - 3]
  );

  if (props.countryColor !== undefined) {
    colourTints.value = ColorTranslator.getTints(props.countryColor, 3);
    fillColour.value = colourTints.value[colourTints.value.length - 1];
  }

  watch(currentTerritory, () => {
    if (currentTerritory.value === props.name) {
      isActive.value = true;
      fillColour.value = colourTints.value[colourTints.value.length - 3];
    } else {
      isActive.value = false;
      fillColour.value = colourTints.value[colourTints.value.length - 1];
    }
  });
</script>

<style scoped>
  @import "@/assets/countries.css";

  g:hover {
    @apply active;
  }

  .l,
  .Unowned {
    fill: #ffffdd;
    stroke: black;
    stroke-linejoin: round;
  }
  .w {
    fill: #99ccff;
    stroke: black;
    stroke-linejoin: round;
  }
  .s {
    fill: #dddddd;
    stroke: black;
    stroke-linejoin: round;
  }

  text {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9px;
  }

  .active {
    stroke-width: 3px;
  }

  text {
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
    user-select: none; /* Standard */
    pointer-events: none;
  }
</style>
