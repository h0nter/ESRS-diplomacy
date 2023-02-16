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
      name: "North Atlantic Ocean",
      polygon: "70,261 64,250 67,242 71,245 81,234 74,228 80,225 78,218 82,217 89,220 94,220 95,218 94,216 97,216 101,212 110,212 119,217 120,227 130,227 130,223 138,217 138,214 130,208 129,197 139,189 140,182 148,177 148,0 0,0 0,273 58,273",
      type: "w",
      text: "NAO",
      textPos: [65, 120]
    },
    {
      name: "Mid-Atlantic Ocean",
      polygon: "102,317 100,322 103,328 109,329 123,344 122,350 123,357 128,363 121,382 122,384 112,399 101,396 96,397 72,384 59,381 54,375 48,374 46,378 39,375 33,381 35,384 32,396 30,406 17,427 14,427 10,433 13,440 15,441 12,450 13,454 8,462 19,469 27,468 33,475 34,484 37,490 37,495 33,496 17,518 0,520 0,273 58,273",
      type: "w",
      text: "MAO",
      textPos: [50, 355]
    },
    {
      name: "Irish Sea",
      polygon: "100,291 112,287 122,281 130,282 127,276 119,272 116,272 115,265 128,262 126,256 121,257 132,250 135,250 139,240 136,229 130,227 120,227 110,232 109,246 98,259 87,257 70,261 58,273 88,303",
      type: "w",
      text: "IRI",
      textPos: [95, 270]
    },
    {
      name: "English Channel",
      polygon: "173,301 169,311 153,315 155,320 150,319 144,318 142,312 136,310 136,326 124,323 122,318 102,317 88,303 100,291 110,292 120,295 124,291 134,294 147,295 160,298 168,296",
      type: "w",
      text: "ENG",
      textPos: [135, 306]
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
      width: 70%;
    }

    svg {
        width: 100%;
        max-width: 100vw;
        max-height: 100vh;
    }
</style>