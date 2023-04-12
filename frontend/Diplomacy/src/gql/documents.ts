import { gql } from "@apollo/client/core";

// Example GraphQL query
export const LOCATIONS = gql`
    query {
        locations {
            id,
            isCoast
        }
    }
`;

export const TERRITORIES = gql`
    query {
        locations {
            id,
            name,
            isCoast,
            isSea,
            abbreviation,
            textPosX,
            textPosY,
            polygons {
                id,
                polygon,
                colour
            },
            currentOwner{
                name
            }
        }
    }
`;

export const UNITS = gql`
    query {
        units {
            id,
            canFloat,
            owner {
                name
            }
            location {
                name,
            }
        }
    }
`;