<template>
  <g :title="name" :id="name" :coast="isCoast"  @mouseenter="$emit('territoryHovered', name)">
    <polygon v-if="polygon1" :class="type1" :points="polygon1"/>
    <polygon v-if="polygon2" :class="type2" :points="polygon2"/>
    <path v-if="path" :class="type1" :d="path"/>
    <text :x="textX" :y="textY">{{ text }}</text>
<!--    <Unit v-if="unit" :type="unit" :transform="'translate('+ (textX + 8) + ', ' + (textY - 14) + ')'"/>-->
    <use v-bind="{'xlink:href' : unit}" :id="name" :class="[country ? country : '']" :transform="'translate(' + (textX + 8) + ', ' + (textY - 14) + ')'"/>
  </g>
</template>

<script setup>
  import Unit from "@/components/Unit.vue";

  const props = defineProps({
    name: String,
    country: String,
    polygon1: String,
    type1: String,
    polygon2: String,
    type2: String,
    path: String,
    isCoast: Boolean,
    text: String,
    textX: Number,
    textY: Number,
    unit: String,
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