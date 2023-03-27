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
        mapPolygon {
            polygon,
            location {
                id,
                name,
                isCoast,
                isSea,
                textPos,
                currentOwner{
                    name
                }
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