import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client/core";

// HTTP connection to the API
const httpLink = new HttpLink({
  uri: "http://127.0.0.1:8080/graphql", // Matches the url and port that Django is using
});

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  connectToDevTools: true,
});
