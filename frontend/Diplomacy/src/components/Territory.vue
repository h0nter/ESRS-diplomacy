<template>
  <g :title="name">
    <polygon :class="type" :points="polygon"/>
    <text :x="textX" :y="textY">{{ text }}</text>
  </g>
</template>

<script setup>
const props = defineProps({
  name: String,
  polygon: String,
  type: String,
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
</style>