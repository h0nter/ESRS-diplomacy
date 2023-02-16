<template>
  <div>
    <svg viewBox="0 0 610 560" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <Territory v-for="territory in territories" :name="territory.name" :polygon="territory.polygon" :type="territory.type" :text="territory.text" :textX="territory.textPos[0]" :textY="territory.textPos[1]"/>
    </svg>
  </div>
</template>

<script setup>
  import Territory from "@/components/Territory.vue";

  const territories = [
    {
      name: "Norwegian Sea",
      polygon: "362,33 357,39 343,44 324,54 320,64 310,75 309,84 303,86 292,111 277,132 269,134 264,142 258,141 236,154 198,154 171,181 171,197 158,193 152,194 154,188 161,185 162,181 148,177 148,0 362,0",
      type: "w",
      text: "NWG",
      textPos: [220, 70]
    },
    {
      name: "North Sea",
      polygon: "M171,197 L171,181 A27,27 0,0,1 198,154 L241,154 L241,224 L248,224 L245,237 L211,237 L211,301 L173,301 L165,293 L140,197Z",
      type: "w",
      text: "NTH",
      textPos: [190, 230]
    },
    {
      name: "Switzerland",
      polygon: "209,363 208,367 194,382 197,385 203,379 207,386 213,387 221,385 227,390 229,385 243,388 245,384 241,378 234,374 234,366 232,363 225,362 222,365",
      type: "s",
      text: "Swi",
      textPos: [215, 378]
    }
  ]
</script>

<style scoped>
    div {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
    }

    svg {
        width: 100%;
        max-width: 100vw;
        max-height: 100vh;
    }
</style>