import { ref } from "vue";
import { defineStore } from "pinia";
import { useGameStore } from "@/stores/GameStore";

export const useMapStore = defineStore("MapStore", () => {
  const gameStore = useGameStore();

  const territoryHovered = ref("#");
  const activeUnit = ref("#");
  const activeUnitMenu = ref("#");
  const activeUnitName = ref("");

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

  const supportHandler = () => {
    _closeActionMenu();
    gameStore.holdHandler();
  };

  const moveHandler = () => {
    _closeActionMenu();
    gameStore.holdHandler();
  };

  const convoyHandler = () => {
    _closeActionMenu();
    gameStore.holdHandler();
  };

  const moveViaConvoyHandler = () => {
    _closeActionMenu();
    gameStore.holdHandler();
  };

  const territoryHoverHandler = (territoryName: string) => {
    territoryHovered.value = "#" + territoryName;
  };

  return {
    territoryHovered,
    activeUnit,
    activeUnitMenu,
    activeUnitName,
    territoryHoverHandler,
    unitClickHandler,
    holdHandler,
    supportHandler,
    moveHandler,
    convoyHandler,
    moveViaConvoyHandler,
  };
});
