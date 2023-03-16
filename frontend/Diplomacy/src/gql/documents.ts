import { gql } from "@apollo/client/core";

// Example GraphQL query
export const UNITS = gql`
    query {
        locations {
            id,
            isCoast
        }
    }
`;