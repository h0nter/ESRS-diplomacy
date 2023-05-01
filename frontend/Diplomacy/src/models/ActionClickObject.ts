import type { RoomOrderInstructionChoices } from "@/gql/graphql";

export type ActionClickObject = {
  actionType: ExtOrderInstructionChoices;
  unitID: Number;
};

export type ExtOrderInstructionChoices = RoomOrderInstructionChoices | "VCV";
