import {
  ApolloClient,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client/core";


// HTTP connection to the API
const httpLink = createHttpLink({
  uri: "http://127.0.0.1:8000/graphql", // Matches the url and port that Django is using
});

// Cache implementation
const cache = new InMemoryCache();

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: httpLink,
  cache,
});