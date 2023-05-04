import { ref } from "vue";
import { defineStore } from "pinia";
import { useGameStore } from "@/stores/GameStore";

export const useMapStore = defineStore("MapStore", () => {
  const gameStore = useGameStore();

  const territoryHovered = ref("#");
  const activeUnit = ref("#");
  const activeUnitMenu = ref("#");
  const activeUnitName = ref("");
  const currentTerritory = ref("");
  const targetTerritory = ref("");

  const unitClickHandler = (unitID: string, unitMenuID: string) => {
    // If the active unit is clicked again, close the menu
    if (unitID === activeUnitName.value) {
      activeUnitName.value = "";
    } else {
      // Otherwise, open the menu (only one open at a time)
      activeUnitName.value = unitID;
    }
    // This here is a stupid hack to force the re-rendering/drawing of the active unit and menu.
    activeUnit.value = "#" + unitID;
    activeUnit.value = "#";
    activeUnitMenu.value = "#" + unitMenuID;
  };

  const _closeActionMenu = () => {
    activeUnitName.value = "";
    activeUnit.value = "#";
    activeUnitMenu.value = "#";
  };

  const holdHandler = () => {
    _closeActionMenu();
    // No need to do anything else
    // Update the active unit's order to Hold
    gameStore.holdHandler();
  };

  const supportHandler = (territoryName: string) => {
    _closeActionMenu();
    // Unit remains in place and supports another unit
    // Begin support action
    // 1. Highlight the current territory in stronger color, and supportable units in thicker border (all units for now - verify this later)
    //    lock clicking on other territories.
    // 2. Click on the unit to support (cancel by clicking on the territory again)
    // 3. Click on the territory to direct the support to (any neighbouring territory)
    // 4. If the unit belongs to the player, update the target unit order to move to the target territory
    // 5. Draw a support (double) arrow from the supporting unit to the target territory
    // 6. Update the order for the unit to support the target unit to the target territory
    currentTerritory.value = territoryName;
    // gameStore.holdHandler();
  };

  const moveHandler = (territoryName: string) => {
    _closeActionMenu();
    // Unit moves one space
    // Begin move action
    // 1. Highlight the current territory in stronger color, and neighbouring territories in thicker border
    //    (data from the backend, should already handle fleets/armies correctly)
    //    lock clicking on other territories.
    // 2. Click on the territory to move to (cancel by clicking on the territory again)
    // 3. Draw move arrow from the unit to the target territory
    // 4. Update the order for the unit to move to the target territory
    currentTerritory.value = territoryName;
    // gameStore.holdHandler();
  };

  const convoyHandler = (territoryName: string) => {
    _closeActionMenu();
    // Fleet convoys an army
    // Begin convoy action
    // 1. Highlight the current territory in stronger color, and supportable units in thicker border (all units for now - verify this later)
    //    lock clicking on other territories.
    // 2. Click on the unit to convoy (cancel by clicking on the territory again)
    // 3. Draw the convoy (dotted) line from the fleet to the unit's move arrow
    // 4. Update the order for the unit to convoy the target unit
    currentTerritory.value = territoryName;
    // gameStore.holdHandler();
  };

  const moveViaConvoyHandler = (territoryName: string) => {
    _closeActionMenu();
    // An Army is convoyed by a fleet
    // Begin convoy action
    // 1. Highlight the current territory in stronger color, and all coastal territories (neighbouring with an army) in thicker border
    //    lock clicking on other territories.
    // 2. Click on the territory to move to (cancel by clicking on the territory again)
    // 3. Draw a move arrow from the unit to the target territory
    // 4. Update the order for the unit to move to the target territory
    currentTerritory.value = territoryName;
    // gameStore.holdHandler();
  };

  const territoryHoverHandler = (territoryName: string) => {
    territoryHovered.value = "#" + territoryName;
  };

  return {
    territoryHovered,
    activeUnit,
    activeUnitMenu,
    activeUnitName,
    currentTerritory,
    targetTerritory,
    territoryHoverHandler,
    unitClickHandler,
    holdHandler,
    supportHandler,
    moveHandler,
    convoyHandler,
    moveViaConvoyHandler,
  };
});
