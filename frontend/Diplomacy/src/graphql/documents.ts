import { gql } from "@apollo/client/core";

const REPO_FRAGMENT = gql`
  fragment repo on Repository {
    id
    name
    url
    stargazers {
      totalCount
    }
    viewerHasStarred
    description
    licenseInfo {
      name
    }
    updatedAt
    owner {
      login
      avatarUrl
    }
    primaryLanguage {
      color
      name
    }
    repositoryTopics(first: 10) {
      edges {
        node {
          topic {
            name
          }
        }
      }
    }
  }
`;