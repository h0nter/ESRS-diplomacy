/* eslint-disable */
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: any;
};

export type CountryType = {
  __typename?: 'CountryType';
  colour: Scalars['String'];
  id: Scalars['ID'];
  locationownerSet: Array<LocationOwnerType>;
  map: MapType;
  name: Scalars['String'];
  playerCountry: Array<PlayerType>;
  unitSet: Array<UnitType>;
};

export type CreateOrder = {
  __typename?: 'CreateOrder';
  order?: Maybe<OrderType>;
};

export type CreatePlayer = {
  __typename?: 'CreatePlayer';
  player?: Maybe<PlayerType>;
};

export type CreateRoom = {
  __typename?: 'CreateRoom';
  room?: Maybe<RoomType>;
};

export type CreateTurn = {
  __typename?: 'CreateTurn';
  turn?: Maybe<TurnType>;
};

export type CreateUnit = {
  __typename?: 'CreateUnit';
  unit?: Maybe<UnitType>;
};

export type LocationOwnerType = {
  __typename?: 'LocationOwnerType';
  currentOwner?: Maybe<CountryType>;
  id: Scalars['ID'];
  location: LocationType;
  room: RoomType;
};

export type LocationType = {
  __typename?: 'LocationType';
  NextToLocation: Array<Next_ToType>;
  abbreviation: Scalars['String'];
  currentLocation: Array<OrderType>;
  id: Scalars['ID'];
  isCoast: Scalars['Boolean'];
  isSea: Scalars['Boolean'];
  locationForPlayer: Array<LocationOwnerType>;
  map: MapType;
  name: Scalars['String'];
  nextTo: Array<Next_ToType>;
  polygons: Array<Map_PolygonType>;
  referenceUnitCurrentLocation: Array<OrderType>;
  referenceUnitNewLocation: Array<OrderType>;
  targetLocation: Array<OrderType>;
  textPosX: Scalars['Int'];
  textPosY: Scalars['Int'];
  unitSet: Array<UnitType>;
  unitSpawn: Scalars['Boolean'];
};

export type MapType = {
  __typename?: 'MapType';
  countrySet: Array<CountryType>;
  id: Scalars['ID'];
  locationSet: Array<LocationType>;
  maxCountries: Scalars['Int'];
  name: Scalars['String'];
  roomMap: Array<RoomType>;
};

export type Map_PolygonType = {
  __typename?: 'Map_PolygonType';
  colour: RoomMap_PolygonColourChoices;
  id: Scalars['ID'];
  location: LocationType;
  polygon: Scalars['String'];
};

export type Mutation = {
  __typename?: 'Mutation';
  createOrder?: Maybe<CreateOrder>;
  createPlayer?: Maybe<CreatePlayer>;
  createRoom?: Maybe<CreateRoom>;
  createTrun?: Maybe<CreateTurn>;
  createUnit?: Maybe<CreateUnit>;
  updateOrder?: Maybe<UpdateOrder>;
};


export type MutationCreateOrderArgs = {
  input: OrderInput;
};


export type MutationCreatePlayerArgs = {
  roomId: Scalars['ID'];
  userId: Scalars['ID'];
};


export type MutationCreateRoomArgs = {
  roomName: Scalars['String'];
};


export type MutationCreateTrunArgs = {
  isAutumn?: InputMaybe<Scalars['Boolean']>;
  year: Scalars['Int'];
};


export type MutationCreateUnitArgs = {
  canFloat?: InputMaybe<Scalars['Boolean']>;
  location?: InputMaybe<Scalars['ID']>;
  owner?: InputMaybe<Scalars['ID']>;
  room?: InputMaybe<Scalars['ID']>;
};


export type MutationUpdateOrderArgs = {
  id?: InputMaybe<Scalars['ID']>;
  input: OrderInput;
};

export type Next_ToType = {
  __typename?: 'Next_toType';
  id: Scalars['ID'];
  location: LocationType;
  nextTo: LocationType;
};

export type OrderInput = {
  instruction: Scalars['String'];
  referenceUnitCurrentLocationId?: InputMaybe<Scalars['ID']>;
  referenceUnitId?: InputMaybe<Scalars['ID']>;
  referenceUnitNewLocationId?: InputMaybe<Scalars['ID']>;
  roomId: Scalars['ID'];
  targetLocationId?: InputMaybe<Scalars['ID']>;
  turnId: Scalars['ID'];
  unitId: Scalars['ID'];
};

export type OrderType = {
  __typename?: 'OrderType';
  currentLocation: LocationType;
  id: Scalars['ID'];
  instruction: RoomOrderInstructionChoices;
  outcomeReferenceToOrder: Array<OutcomeType>;
  referenceUnit?: Maybe<UnitType>;
  referenceUnitCurrentLocation?: Maybe<LocationType>;
  referenceUnitNewLocation?: Maybe<LocationType>;
  room: RoomType;
  targetLocation?: Maybe<LocationType>;
  turn: TurnType;
  unit: UnitType;
};

export type OutcomeType = {
  __typename?: 'OutcomeType';
  id: Scalars['ID'];
  orderReference: OrderType;
  validation: RoomOutcomeValidationChoices;
};

export type PlayerType = {
  __typename?: 'PlayerType';
  country?: Maybe<CountryType>;
  id: Scalars['ID'];
  isAlive: Scalars['Boolean'];
  isFinished: Scalars['Boolean'];
  room: RoomType;
  userId: Scalars['Int'];
};

export type Query = {
  __typename?: 'Query';
  country?: Maybe<Array<Maybe<CountryType>>>;
  location?: Maybe<Array<Maybe<LocationType>>>;
  locationOwner?: Maybe<Array<Maybe<LocationOwnerType>>>;
  map?: Maybe<Array<Maybe<MapType>>>;
  mapPolygon?: Maybe<Array<Maybe<Map_PolygonType>>>;
  nextTo?: Maybe<Array<Maybe<Next_ToType>>>;
  order?: Maybe<Array<Maybe<OrderType>>>;
  outcome?: Maybe<Array<Maybe<OutcomeType>>>;
  player?: Maybe<Array<Maybe<PlayerType>>>;
  room?: Maybe<Array<Maybe<RoomType>>>;
  turn?: Maybe<Array<Maybe<TurnType>>>;
  unit?: Maybe<Array<Maybe<UnitType>>>;
};


export type QueryOrderArgs = {
  roomId?: InputMaybe<Scalars['Int']>;
  turnId?: InputMaybe<Scalars['Int']>;
  unitId?: InputMaybe<Scalars['Int']>;
};


export type QueryPlayerArgs = {
  userId?: InputMaybe<Scalars['Int']>;
};


export type QueryRoomArgs = {
  playerId?: InputMaybe<Scalars['Int']>;
};


export type QueryTurnArgs = {
  roomId?: InputMaybe<Scalars['Int']>;
};

/** An enumeration. */
export enum RoomMap_PolygonColourChoices {
  /** AQUA */
  Aqua = 'AQUA',
  /** HASH */
  Hash = 'HASH',
  /** LAND */
  Land = 'LAND'
}

/** An enumeration. */
export enum RoomOrderInstructionChoices {
  /** Convoy */
  Cvy = 'CVY',
  /** Hold */
  Hld = 'HLD',
  /** Move */
  Mve = 'MVE',
  /** Support */
  Spt = 'SPT'
}

/** An enumeration. */
export enum RoomOutcomeValidationChoices {
  /** Order Bounced with another */
  Bnce = 'BNCE',
  /** Order Cut */
  Cut = 'CUT',
  /** Order Unit needs to Disband */
  Dban = 'DBAN',
  /** Order Unit Dislodged */
  Dlge = 'DLGE',
  /** Convoy Order Distrupted */
  Drpt = 'DRPT',
  /** Order Marked for future Evaluation */
  Mark = 'MARK',
  /** Order Not Evaluated */
  Mybe = 'MYBE',
  /** Move Order has No Convoy */
  Ncvy = 'NCVY',
  /** Order Passed */
  Pass = 'PASS',
  /** Order Failed */
  Void = 'VOID'
}

/** An enumeration. */
export enum RoomRoomStatusChoices {
  /** Check the closing conditions */
  Check = 'CHECK',
  /** Will only change the status when room is closed */
  Closed = 'CLOSED',
  /** registered */
  Registerd = 'REGISTERD',
  /** Resolving Orders */
  Resolve = 'RESOLVE',
  /** Gaining Units After FALL */
  Resupp = 'RESUPP',
  /** Orders Incoming, Only Players Retreating */
  Retreat = 'RETREAT',
  /** Update map with new Unit Positions */
  Update = 'UPDATE',
  /** Orders Incoming, Players Debating */
  Wait = 'WAIT'
}

export type RoomType = {
  __typename?: 'RoomType';
  closeTime?: Maybe<Scalars['DateTime']>;
  currentTurn?: Maybe<TurnType>;
  id: Scalars['ID'];
  locationownerSet: Array<LocationOwnerType>;
  map: MapType;
  playrJoinedRoom: Array<PlayerType>;
  roomName: Scalars['String'];
  roomOder: Array<OrderType>;
  status: RoomRoomStatusChoices;
  unitSet: Array<UnitType>;
};

export type TurnType = {
  __typename?: 'TurnType';
  currentTurn: Array<RoomType>;
  id: Scalars['ID'];
  isAutumn: Scalars['Boolean'];
  isRetreatTurn: Scalars['Boolean'];
  orderSet: Array<OrderType>;
  year: Scalars['Int'];
};

export type UnitType = {
  __typename?: 'UnitType';
  canFloat: Scalars['Boolean'];
  id: Scalars['ID'];
  location: LocationType;
  owner: CountryType;
  referenceUnit: Array<OrderType>;
  room: RoomType;
  targetUnit: Array<OrderType>;
};

export type UpdateOrder = {
  __typename?: 'UpdateOrder';
  ok?: Maybe<Scalars['Boolean']>;
  order?: Maybe<OrderType>;
};
