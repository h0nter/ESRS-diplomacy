import { ref } from "vue";
import { defineStore } from "pinia";
import { useGameStore } from "@/stores/GameStore";
import type { LocationType } from "@/gql/graphql";
import { RoomOrderInstructionChoices } from "@/gql/graphql";

export const useMapStore = defineStore("MapStore", () => {
  const gameStore = useGameStore();

  const ERROR_DELAY = 5000;
  const orderTargetUnitName = ref("#");

  const territoryHovered = ref("#");
  const errorUnit = ref("#");
  const activeUnit = ref("#");
  const activeUnitMenu = ref("#");
  const activeUnitName = ref("");
  const currentTerritory = ref("");
  const targetTerritory = ref("");

  const referenceUnitID = ref<string>("");
  const referenceUnitCurrentTerritory = ref<string>("");
  const referenceUnitTargetTerritory = ref<string>("");

  const moveOrder = ref<boolean>(false);
  const supportOrder = ref<boolean>(false);
  const convoyOrder = ref<boolean>(false);
  const moveViaConvoyOrder = ref<boolean>(false);
  const submittingOrder = ref<boolean>(false);

  const unitClickHandler = (unitID: string, unitMenuID: string) => {
    // If the active unit is clicked again, close the menu
    if (unitID === activeUnitName.value) {
      activeUnitName.value = "";
      orderTargetUnitName.value = "";
    } else {
      // Otherwise, open the menu (only one open at a time)
      activeUnitName.value = unitID;
      orderTargetUnitName.value = unitID;
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

  const _resetOrderState = () => {
    // Reset the state for the next order
    currentTerritory.value = "";
    targetTerritory.value = "";
    referenceUnitID.value = "";
    referenceUnitCurrentTerritory.value = "";
    referenceUnitTargetTerritory.value = "";
    orderTargetUnitName.value = "";
  };

  const _showUnitError = async (unitID: string) => {
    errorUnit.value = unitID;
    await new Promise((r) => setTimeout(r, ERROR_DELAY));
    errorUnit.value = "#";
  };

  const holdHandler = async () => {
    _closeActionMenu();
    // No need to do anything else
    // Update the active unit's order to Hold
    // Submit the order
    submittingOrder.value = true;
    const order_ok = await gameStore.updateOrder(
      RoomOrderInstructionChoices.Hld
    );
    submittingOrder.value = false;

    if (!order_ok) {
      _showUnitError(orderTargetUnitName.value);
    }

    _resetOrderState();
  };

  const supportHandler = async (
    territoryID: string,
    territoryName: string,
    newSupport: Boolean,
    unitID: string = ""
  ) => {
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
    // gameStore.holdHandler();
    if (newSupport) {
      currentTerritory.value = territoryName;
      gameStore.currentLocationID = parseInt(territoryID);
      supportOrder.value = true;
    } else if (supportOrder.value && unitID !== "") {
      referenceUnitID.value = unitID;
      referenceUnitCurrentTerritory.value = territoryName;
      gameStore.referenceUnitID = parseInt(unitID);
      gameStore.referenceUnitCurrentLocationID = parseInt(territoryID);
    } else {
      referenceUnitTargetTerritory.value = territoryName;
      gameStore.referenceUnitTargetLocationID = parseInt(territoryID);
      supportOrder.value = false;

      // Submit the order
      submittingOrder.value = true;
      const order_ok = await gameStore.updateOrder(
        RoomOrderInstructionChoices.Spt
      );
      submittingOrder.value = false;

      // Arrows are drawn from the orders returned by the backend

      if (!order_ok) {
        _showUnitError(orderTargetUnitName.value);
      }

      _resetOrderState();
    }
  };

  const moveHandler = async (
    territoryID: string,
    territoryName: string,
    newMove: Boolean
  ) => {
    _closeActionMenu();
    // Unit moves one space
    // Begin move action
    // 1. Highlight the current territory in stronger color, and neighbouring territories in thicker border
    //    (data from the backend, should already handle fleets/armies correctly)
    //    lock clicking on other territories.
    // 2. Click on the territory to move to (cancel by clicking on the territory again)
    // 3. Draw move arrow from the unit to the target territory
    // 4. Update the order for the unit to move to the target territory

    // Decide if we're starting a new move order or continue an existing one
    if (newMove) {
      currentTerritory.value = territoryName;
      gameStore.currentLocationID = parseInt(territoryID);
      moveOrder.value = true;
    } else {
      targetTerritory.value = territoryName;
      gameStore.targetLocationID = parseInt(territoryID);
      moveOrder.value = false;

      // Submit the order
      submittingOrder.value = true;
      const order_ok = await gameStore.updateOrder(
        RoomOrderInstructionChoices.Mve
      );
      submittingOrder.value = false;

      if (!order_ok) {
        _showUnitError(orderTargetUnitName.value);
      }

      _resetOrderState();
    }
  };

  const convoyHandler = async (
    territoryID: string,
    territoryName: string,
    newConvoy: Boolean,
    unitID: string = ""
  ) => {
    _closeActionMenu();
    // Fleet convoys an army
    // Begin convoy action
    // 1. Highlight the current territory in stronger color, and supportable units in thicker border (all units for now - verify this later)
    //    lock clicking on other territories.
    // 2. Click on the unit to convoy (cancel by clicking on the territory again)
    // 3. Draw the convoy (dotted) line from the fleet to the unit's move arrow
    // 4. Update the order for the unit to convoy the target unit
    if (newConvoy) {
      currentTerritory.value = territoryName;
      gameStore.currentLocationID = parseInt(territoryID);
      convoyOrder.value = true;
    } else if (convoyOrder.value && unitID !== "") {
      referenceUnitID.value = unitID;
      referenceUnitCurrentTerritory.value = territoryName;
      gameStore.referenceUnitID = parseInt(unitID);
      gameStore.referenceUnitCurrentLocationID = parseInt(territoryID);
    } else {
      referenceUnitTargetTerritory.value = territoryName;
      gameStore.referenceUnitTargetLocationID = parseInt(territoryID);
      convoyOrder.value = false;

      // Submit the order
      submittingOrder.value = true;
      const order_ok = await gameStore.updateOrder(
        RoomOrderInstructionChoices.Cvy
      );
      submittingOrder.value = false;

      // Arrows are drawn from the orders returned by the backend

      if (!order_ok) {
        _showUnitError(orderTargetUnitName.value);
      }

      _resetOrderState();
    }
  };

  const moveViaConvoyHandler = async (
    territoryID: string,
    territoryName: string,
    newConvoyMove: Boolean
  ) => {
    _closeActionMenu();
    // An Army is convoyed by a fleet
    // Begin convoy action
    // 1. Highlight the current territory in stronger color, and all coastal territories (neighbouring with an army) in thicker border
    //    lock clicking on other territories.
    // 2. Click on the territory to move to (cancel by clicking on the territory again)
    // 3. Draw a move arrow from the unit to the target territory
    // 4. Update the order for the unit to move to the target territory
    if (newConvoyMove) {
      currentTerritory.value = territoryName;
      gameStore.currentLocationID = parseInt(territoryID);
      moveViaConvoyOrder.value = true;
    } else {
      targetTerritory.value = territoryName;
      gameStore.targetLocationID = parseInt(territoryID);
      moveViaConvoyOrder.value = false;

      // Submit the order
      submittingOrder.value = true;
      const order_ok = await gameStore.updateOrder(
        RoomOrderInstructionChoices.Mve
      );
      submittingOrder.value = false;

      // Arrows are drawn from the orders returned by the backend

      if (!order_ok) {
        _showUnitError(orderTargetUnitName.value);
      }

      _resetOrderState();
    }
  };

  const territoryHoverHandler = (territoryName: string) => {
    territoryHovered.value = "#" + territoryName;
  };

  return {
    territoryHovered,
    errorUnit,
    activeUnit,
    activeUnitMenu,
    activeUnitName,
    currentTerritory,
    targetTerritory,
    referenceUnitID,
    referenceUnitCurrentTerritory,
    referenceUnitTargetTerritory,
    moveOrder,
    supportOrder,
    convoyOrder,
    moveViaConvoyOrder,
    submittingOrder,
    territoryHoverHandler,
    unitClickHandler,
    holdHandler,
    supportHandler,
    moveHandler,
    convoyHandler,
    moveViaConvoyHandler,
  };
});
