<template>
  <g :title="name" :id="'territory-' + name" :coast="isCoast"  @mouseenter="$emit('territoryHovered', name)">
    <polygon v-for="polygon in polygons" :key="polygon.id" :class="polygon.colour === PolygonColourChoices.Land ? 'l' : 'w' " :points="polygon.polygon"/>
    <text :x="textX" :y="textY">{{ text }}</text>
<!--    <Unit v-if="unit" :type="unit" :transform="'translate('+ (textX + 8) + ', ' + (textY - 14) + ')'"/>-->
    <use v-bind="{'xlink:href' : linkedUnit.ref.value}" :id="name + '-unit-slot'" :style="'fill:' + linkedUnit.color" :transform="'translate(' + (textX + 8) + ', ' + (textY - 14) + ')'" />
  </g>

<!--  v-bind="{'xlink:href' : unit}"-->
</template>

<script lang="ts" setup>
import {PropType, ref, Ref, watchEffect} from "vue";
  import type {Map_PolygonType, UnitType} from "@/gql/graphql";
  import { RoomMap_PolygonColourChoices } from "@/gql/graphql";

  const props = defineProps({
    name: String,
    country: String,
    polygons: Array as PropType<Map_PolygonType[]>,
    isCoast: Boolean,
    text: String,
    textX: Number,
    textY: Number,
    units: Array as PropType<UnitType[]>,
  });

  type Unit = {
    ref: Ref<string>,
    color: String,
}

  const PolygonColourChoices : any = RoomMap_PolygonColourChoices;
  const linkedUnit : Unit = {ref : ref("#")} as Unit;

  watchEffect(() => {
    if (props.units && props.units.length > 0) {
      props.units.forEach((unit) => {
        if (unit.location.name === props.name) {
          if (unit.canFloat) {
            linkedUnit.ref.value = "#F";
          } else {
            linkedUnit.ref.value = "#A";
          }
          linkedUnit.color = unit.owner.colour;
        }
      })
    }
  });
</script>

<style scoped>
    @import "@/assets/countries.css";

    g:hover{
      @apply active
    }

  	.l, .Unowned	{fill:#FFFFDD; stroke:black; stroke-linejoin:round}
    .w		{fill:#99CCFF; stroke:black; stroke-linejoin:round}
    .s		{fill:#DDDDDD; stroke:black; stroke-linejoin:round}

    text {font-family:Arial,Helvetica,sans-serif; font-size:8px}

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