export enum RoomStatus {
  REGISTERED = "REGISTERD",
  INITIALIZE = "INITIALIZE",
  WAITING = "WAIT",
  RESOLVE = "RESOLVE",
  RETREAT = "RETREAT",
  UPDATE = "UPDATE",
  RESUPPLY = "RESUPP",
  CHECKING = "CHECK",

  CLOSED = "CLOSED",
}

export type HostData = {
  id: Number;
  room_name: String;
  room_code: String;
  room_status: RoomStatus;
  room_id: Number;
  max_players: Number;
  ip: String;
  port: Number;
  hoster: Number;
};

export type PlayerData = {
  user_id: Number;
  username: String;
};
