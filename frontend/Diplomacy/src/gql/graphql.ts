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
};

export type LocationType = {
  __typename?: 'LocationType';
  currentLocation: Array<OrderType>;
  id: Scalars['ID'];
  isCoast: Scalars['Boolean'];
  isSea: Scalars['Boolean'];
  name: Scalars['String'];
  referenceUnitCurrentLocation: Array<OrderType>;
  referenceUnitNewLocation: Array<OrderType>;
  targetLocation: Array<OrderType>;
  textPos: Scalars['String'];
  unitSet: Array<UnitType>;
  unitSpawn: Scalars['Boolean'];
};

export type Mutation = {
  __typename?: 'Mutation';
  updateOrder?: Maybe<UpdateOrder>;
};


export type MutationUpdateOrderArgs = {
  id?: InputMaybe<Scalars['ID']>;
  input: OrderInput;
};

export type OrderInput = {
  currentLocation: Scalars['Int'];
  instruction: Scalars['String'];
  referenceUnitCurrentLocationPk?: InputMaybe<Scalars['Int']>;
  referenceUnitNewLocationPk?: InputMaybe<Scalars['Int']>;
  referenceUnitPk?: InputMaybe<Scalars['Int']>;
  targetUnit: Scalars['Int'];
  turn: Scalars['Int'];
};

export type OrderType = {
  __typename?: 'OrderType';
  currentLocation: LocationType;
  id: Scalars['ID'];
  instruction: RoomOrderInstructionChoices;
  referenceUnit?: Maybe<UnitType>;
  referenceUnitCurrentLocation?: Maybe<LocationType>;
  referenceUnitNewLocation?: Maybe<LocationType>;
  targetLocation?: Maybe<LocationType>;
  targetUnit: UnitType;
  turn: TurnType;
};

export type OutcomeType = {
  __typename?: 'OutcomeType';
  currentLocation: LocationType;
  id: Scalars['ID'];
  instruction: RoomOrderInstructionChoices;
  referenceUnit?: Maybe<UnitType>;
  referenceUnitCurrentLocation?: Maybe<LocationType>;
  referenceUnitNewLocation?: Maybe<LocationType>;
  targetLocation?: Maybe<LocationType>;
  targetUnit: UnitType;
  turn: TurnType;
};

export type Query = {
  __typename?: 'Query';
  locations?: Maybe<Array<Maybe<LocationType>>>;
  orders?: Maybe<Array<Maybe<OrderType>>>;
  outcomes?: Maybe<Array<Maybe<OutcomeType>>>;
  turns?: Maybe<Array<Maybe<TurnType>>>;
  units?: Maybe<Array<Maybe<UnitType>>>;
};


export type QueryOrdersArgs = {
  orderId?: InputMaybe<Scalars['Int']>;
};

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

export type TurnType = {
  __typename?: 'TurnType';
  id: Scalars['ID'];
  isAutumn: Scalars['Boolean'];
  orderSet: Array<OrderType>;
  year: Scalars['Int'];
};

export type UnitType = {
  __typename?: 'UnitType';
  canFloat: Scalars['Boolean'];
  id: Scalars['ID'];
  location: LocationType;
  referenceUnit: Array<OrderType>;
  targetUnit: Array<OrderType>;
};

export type UpdateOrder = {
  __typename?: 'UpdateOrder';
  ok?: Maybe<Scalars['Boolean']>;
  order?: Maybe<OrderType>;
};
