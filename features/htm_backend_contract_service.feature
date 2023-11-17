@regression @contracts
Feature: HNM Backend Contract Service

  Scenario: "List Of Contracts Created Of User" returns the list of contracts created of user
    Given send POST request to "{base_url}/backend/v1/contracts/created/of/user/list"
    Then assert response code is 200
    Then validate response by "contracts_created" schema

  Scenario Outline: "List Of Contracts Created Of User" returns "Method Not Allowed" in case of <method> method
  Generates the review NFT ID
    Given send <method> request to "{base_url}/backend/v1/contracts/created/of/user/list"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method |
      | GET    |
      | PUT    |
      | DELETE |

  Scenario Outline: "Contract <contract> Info For Deploy" returns the info about contract <contract> deploy
    Given send GET request to "{base_url}/backend/v1/<contract>/info/for/deploy"
    Then assert response code is 200
    Then validate response by "<contract>_info" schema

    Examples:
      | contract |
      | erc1155  |
      | erc721   |

  Scenario Outline: "Contract <contract> Info For Deploy" returns "Method Not Allowed" in case of <method> method
    Given send <method> request to "{base_url}/backend/v1/<contract>/info/for/deploy"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | contract | method |
      | erc1155  | POST   |
      | erc1155  | PUT    |
      | erc1155  | DELETE |
      | erc721   | POST   |
      | erc721   | PUT    |
      | erc721   | DELETE |

  Scenario: "Contract Info For Deploy" returns an error in case of invalid contract
    Given send GET request to "{base_url}/backend/v1/invalid/info/for/deploy"
    Then assert response code is 200
    Then reason "Not Found" message presence in response
    Then validate response by "validation_error" schema
