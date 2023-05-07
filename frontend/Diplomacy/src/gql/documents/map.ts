import { gql } from "@apollo/client/core";

export const INITIAL_MAP_SETUP = gql`
  query {
    locations {
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
      currentOwner {
        name
        colour
      }
    }
    units {
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
    units {
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
    orders {
      id
      instruction
      turn {
        id
      }
      targetUnit {
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
    turns {
      id
      isAutumn
    }
  }
`;

export const UPDATE_ORDER = gql`
  mutation UpdateOrder(
    $unitID: Int!
    $instruction: String!
    $turnID: Int!
    $currentLocation: Int!
    $orderID: ID!
    $targetLocation: Int = null
    $referenceUnitID: Int = null
    $referenceUnitCurrentLocation: Int = null
    $referenceUnitTargetLocation: Int = null
  ) {
    updateOrder(
      input: {
        instruction: $instruction
        targetUnit: $unitID
        turn: $turnID
        currentLocation: $currentLocation
        targetLocation: $targetLocation
        referenceUnitPk: $referenceUnitID
        referenceUnitCurrentLocationPk: $referenceUnitCurrentLocation
        referenceUnitNewLocationPk: $referenceUnitTargetLocation
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
        targetUnit {
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
