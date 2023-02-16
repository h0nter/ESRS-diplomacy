<template>
  <g :title="name">
    <polygon v-if="polygon1" :class="type1" :points="polygon1"/>
    <polygon v-if="polygon2" :class="type2" :points="polygon2"/>
    <path v-if="path" :class="type1" :d="path"/>
    <text :x="textX" :y="textY">{{ text }}</text>
  </g>
</template>

<script setup>
const props = defineProps({
  name: String,
  polygon1: String,
  type1: String,
  polygon2: String,
  type2: String,
  path: String,
  text: String,
  textX: Number,
  textY: Number,
})
</script>

<style scoped>
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

    .Austria	{fill:#FF0000; stroke:black}
    .England	{fill:#0000FF; stroke:black}
    .France 	{fill:#00FFFF; stroke:black}
    .Germany	{fill:#808080; stroke:black}
    .Italy  	{fill:#00FF00; stroke:black}
    .Russia 	{fill:#008000; stroke:black}
    .Turkey 	{fill:#FFFF00; stroke:black}

    text {
      -webkit-user-select: none; /* Safari */        
      -moz-user-select: none; /* Firefox */
      -ms-user-select: none; /* IE10+/Edge */
      user-select: none; /* Standard */
      pointer-events: none;
    }
</style>