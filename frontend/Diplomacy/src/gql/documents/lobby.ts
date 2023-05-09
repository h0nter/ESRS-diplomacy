import { gql } from "@apollo/client/core";

export const LOBBY_DATA = gql`
  query RoomAndPlayers($roomId: ID!) {
    room(roomId: $roomId) {
      id
      roomName
      status
      map {
        id
      }
    }
    player(roomId: $roomId) {
      id
      userId
      country {
        id
        name
      }
    }
  }
`;

export const MAP_NAMES = gql`
  query MapNames($mapId: ID!) {
    map(mapId: $mapId) {
      name
    }
  }
`;

// export const LOBBY_PLAYER_DATA = gql`
//   query Player($roomId: ID!) {
//     player(roomId: $roomId) {
//       id
//       userId
//       country {
//         id
//         name
//       }
//     }
//   }
// `;
