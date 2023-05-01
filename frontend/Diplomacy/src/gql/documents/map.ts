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
