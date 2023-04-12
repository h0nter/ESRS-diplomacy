<template>
  <g :title="name" :id="name" :coast="isCoast"  @mouseenter="$emit('territoryHovered', name)">
    <polygon v-for="polygon in polygons" :key="polygon.id" :class="polygon.colour === PolygonColourChoices.Land ? 'l' : 'w' " :points="polygon.polygon"/>
    <text :x="textX" :y="textY">{{ text }}</text>
<!--    <Unit v-if="unit" :type="unit" :transform="'translate('+ (textX + 8) + ', ' + (textY - 14) + ')'"/>-->
    <use v-bind="{'xlink:href' : unit}" :id="name" :class="[country ? country : '']" :transform="'translate(' + (textX + 8) + ', ' + (textY - 14) + ')'"/>
  </g>
</template>

<script lang="ts" setup>
  import Unit from "@/components/Unit.vue";
  import { PropType } from "vue";
  import type { Map_PolygonType } from "@/gql/graphql";
  import { RoomMap_PolygonColourChoices } from "@/gql/graphql";

  const props = defineProps({
    name: String,
    country: String,
    polygons: Array as PropType<Map_PolygonType[]>,
    isCoast: Boolean,
    text: String,
    textX: Number,
    textY: Number,
    unit: String,
  });

  const PolygonColourChoices : any = RoomMap_PolygonColourChoices;
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