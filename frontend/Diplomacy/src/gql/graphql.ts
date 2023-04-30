/* eslint-disable */
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = {
  [K in keyof T]: T[K];
};
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]?: Maybe<T[SubKey]>;
};
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]: Maybe<T[SubKey]>;
};
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type CountryType = {
  __typename?: "CountryType";
  colour: Scalars["String"];
  id: Scalars["ID"];
  locationSet: Array<LocationType>;
  map: MapType;
  name: Scalars["String"];
  unitSet: Array<UnitType>;
};

export type LocationType = {
  __typename?: "LocationType";
  abbreviation: Scalars["String"];
  currentLocation: Array<OrderType>;
  currentOwner?: Maybe<CountryType>;
  id: Scalars["ID"];
  isCoast: Scalars["Boolean"];
  isSea: Scalars["Boolean"];
  location: Array<Next_ToType>;
  map: MapType;
  name: Scalars["String"];
  nextTo: Array<Next_ToType>;
  polygons: Array<Map_PolygonType>;
  referenceUnitCurrentLocation: Array<OrderType>;
  referenceUnitNewLocation: Array<OrderType>;
  targetLocation: Array<OrderType>;
  textPosX: Scalars["Int"];
  textPosY: Scalars["Int"];
  unitSet: Array<UnitType>;
  unitSpawn: Scalars["Boolean"];
};

export type MapType = {
  __typename?: "MapType";
  countrySet: Array<CountryType>;
  id: Scalars["ID"];
  locationSet: Array<LocationType>;
  maxCountries: Scalars["Int"];
  name: Scalars["String"];
};

export type Map_PolygonType = {
  __typename?: "Map_PolygonType";
  colour: RoomMap_PolygonColourChoices;
  id: Scalars["ID"];
  location: LocationType;
  polygon: Scalars["String"];
};

export type Mutation = {
  __typename?: "Mutation";
  updateOrder?: Maybe<UpdateOrder>;
};

export type MutationUpdateOrderArgs = {
  id?: InputMaybe<Scalars["ID"]>;
  input: OrderInput;
};

export type Next_ToType = {
  __typename?: "Next_toType";
  id: Scalars["ID"];
  location: LocationType;
  nextTo: LocationType;
};

export type OrderInput = {
  currentLocation: Scalars["Int"];
  instruction: Scalars["String"];
  referenceUnitCurrentLocationPk?: InputMaybe<Scalars["Int"]>;
  referenceUnitNewLocationPk?: InputMaybe<Scalars["Int"]>;
  referenceUnitPk?: InputMaybe<Scalars["Int"]>;
  targetUnit: Scalars["Int"];
  turn: Scalars["Int"];
};

export type OrderType = {
  __typename?: "OrderType";
  currentLocation: LocationType;
  id: Scalars["ID"];
  instruction: RoomOrderInstructionChoices;
  orderReference: Array<OutcomeType>;
  referenceUnit?: Maybe<UnitType>;
  referenceUnitCurrentLocation?: Maybe<LocationType>;
  referenceUnitNewLocation?: Maybe<LocationType>;
  targetLocation?: Maybe<LocationType>;
  targetUnit: UnitType;
  turn: TurnType;
};

export type OutcomeType = {
  __typename?: "OutcomeType";
  id: Scalars["ID"];
  orderReference: OrderType;
  validation: Scalars["Boolean"];
};

export type Query = {
  __typename?: "Query";
  country?: Maybe<Array<Maybe<CountryType>>>;
  locations?: Maybe<Array<Maybe<LocationType>>>;
  map?: Maybe<Array<Maybe<MapType>>>;
  mapPolygon?: Maybe<Array<Maybe<Map_PolygonType>>>;
  nextTo?: Maybe<Array<Maybe<Next_ToType>>>;
  orders?: Maybe<Array<Maybe<OrderType>>>;
  outcomes?: Maybe<Array<Maybe<OutcomeType>>>;
  turns?: Maybe<Array<Maybe<TurnType>>>;
  units?: Maybe<Array<Maybe<UnitType>>>;
};

export type QueryOrdersArgs = {
  orderId?: InputMaybe<Scalars["Int"]>;
};

/** An enumeration. */
export enum RoomMap_PolygonColourChoices {
  /** AQUA */
  Aqua = "AQUA",
  /** HASH */
  Hash = "HASH",
  /** LAND */
  Land = "LAND",
}

/** An enumeration. */
export enum RoomOrderInstructionChoices {
  /** Convoy */
  Cvy = "CVY",
  /** Hold */
  Hld = "HLD",
  /** Move */
  Mve = "MVE",
  /** Support */
  Spt = "SPT",
}

export type TurnType = {
  __typename?: "TurnType";
  id: Scalars["ID"];
  isAutumn: Scalars["Boolean"];
  orderSet: Array<OrderType>;
  year: Scalars["Int"];
};

export type UnitType = {
  __typename?: "UnitType";
  canFloat: Scalars["Boolean"];
  id: Scalars["ID"];
  location: LocationType;
  owner: CountryType;
  referenceUnit: Array<OrderType>;
  targetUnit: Array<OrderType>;
};

export type UpdateOrder = {
  __typename?: "UpdateOrder";
  ok?: Maybe<Scalars["Boolean"]>;
  order?: Maybe<OrderType>;
};
