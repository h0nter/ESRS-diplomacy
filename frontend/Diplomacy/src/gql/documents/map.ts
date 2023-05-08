import { gql } from "@apollo/client/core";

export const INITIAL_MAP_SETUP = gql`
  query {
    location {
      id
      name
      isCoast
      isSea
      abbreviation
      textPosX
      textPosY
      polygons {
        id
        polygon
        colour
      }
      locationForPlayer {
        currentOwner {
          name
          colour
        }
      }
    }
    unit {
      id
      canFloat
      owner {
        name
        colour
      }
      location {
        id
        name
        isSea
        isCoast
        textPosX
        textPosY
      }
    }
  }
`;

export const UNITS = gql`
  query {
    unit {
      id
      canFloat
      owner {
        name
      }
      location {
        name
      }
    }
  }
`;

export const PLAYER_ORDERS = gql`
  query {
    order {
      id
      instruction
      turn {
        id
      }
      unit {
        id
      }
      currentLocation {
        id
        textPosX
        textPosY
      }
      targetLocation {
        id
        textPosX
        textPosY
      }
      referenceUnit {
        id
      }
      referenceUnitCurrentLocation {
        id
        textPosX
        textPosY
      }
      referenceUnitNewLocation {
        id
        textPosX
        textPosY
      }
    }
  }
`;

export const TURNS = gql`
  query {
    turn {
      id
      isAutumn
    }
  }
`;

export const UPDATE_ORDER = gql`
  mutation UpdateOrder(
    $unitID: ID!
    $instruction: String!
    $turnID: ID!
    $orderID: ID!
    $roomID: ID = 1
    $targetLocation: ID = null
    $referenceUnitID: ID = null
    $referenceUnitCurrentLocation: ID = null
    $referenceUnitTargetLocation: ID = null
  ) {
    updateOrder(
      input: {
        instruction: $instruction
        unitId: $unitID
        turnId: $turnID
        roomId: $roomID
        targetLocationId: $targetLocation
        referenceUnitId: $referenceUnitID
        referenceUnitCurrentLocationId: $referenceUnitCurrentLocation
        referenceUnitNewLocationId: $referenceUnitTargetLocation
      }
      id: $orderID
    ) {
      ok
      order {
        id
        instruction
        turn {
          id
        }
        unit {
          id
        }
        currentLocation {
          id
          textPosX
          textPosY
        }
        targetLocation {
          id
          textPosX
          textPosY
        }
        referenceUnit {
          id
        }
        referenceUnitCurrentLocation {
          id
          textPosX
          textPosY
        }
        referenceUnitNewLocation {
          id
          textPosX
          textPosY
        }
      }
    }
  }
`;
