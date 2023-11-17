@regression @nfts
Feature: HNM Backend NFTs

  Scenario: "Review Items List" returns list with review requests
    Given send POST request to "{base_url}/backend/v1/nft/{chain_id}/listing/fixed-price/list" with "pending_nft_listing_fixed_price" data
    Then assert response code is 200
    Then validate response by "list_with_review_requests" schema

  Scenario: "Review Items List" returns error in case of invalid chain ID
    Given send POST request to "{base_url}/backend/v1/nft/54321/listing/fixed-price/list" with "pending_nft_listing_fixed_price" data
    Then assert response code is 400
    Then reason "chain ID must be valid" message presence in response
    Then validate response by "validation_error" schema

  Scenario Outline: "Review Items List" returns "Method Not Allowed" in case of <method> method
    Given send <method> request to "{base_url}/backend/v1/nft/{chain_id}/listing/fixed-price/list" with "pending_nft_listing_fixed_price" data
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method |
      | GET    |
      | DELETE |
      | PUT    |

  Scenario: "NFT Statistics" returns the overall statistics of the marketplace
    Given send POST request to "{base_url}/backend/v1/nft/{chain_id}/statistics" with "nft_statistics" data
    Then assert response code is 200
    Then validate response by "nft_statistics" schema

  Scenario: "NFT Statistics" returns an error in case with invalid chain ID
    Given send POST request to "{base_url}/backend/v1/nft/invalid/statistics" with "nft_statistics" data
    Then assert response code is 400
    Then reason "ChainID: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario Outline: "NFT Statistics" returns "Method Not Allowed" in case of <method> method
    Given send <method> request to "{base_url}/backend/v1/nft/invalid/statistics" with "nft_statistics" data
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method |
      | GET    |
      | DELETE |
      | PUT    |

  Scenario: "NFT Statistics" returns an error in case with invalid period start
    Given send POST request to "{base_url}/backend/v1/nft/54211/statistics" with "nft_statistics_invalid_period_start" data
    Then assert response code is 400
    Then reason "PeriodStart: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "NFT Statistics" returns an error in case with invalid period end
    Given send POST request to "{base_url}/backend/v1/nft/54211/statistics" with "nft_statistics_invalid_period_end" data
    Then assert response code is 400
    Then reason "PeriodEnd: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "NFT Statistics" returns an error in case with invalid reverted_period
    Given send POST request to "{base_url}/backend/v1/nft/54211/statistics" with "nft_statistics_reverted_period" data
    Then assert response code is 400
    Then reason "PeriodEnd: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Nft Whitelist" returns list of nft whitelist
    Given send POST request to "{base_url}/backend/v1/nft/{chain_id}/whitelist" with "nft_whitelist" data
    Then assert response code is 200
    Then validate response by "nft_whitelist" schema

  Scenario: "Nft Whitelist" returns error with invalid chain ID
    Given send POST request to "{base_url}/backend/v1/nft/invalid/whitelist" with "nft_whitelist" data
    Then assert response code is 400
    Then reason "chain ID must be valid" message presence in response
    Then validate response by "validation_error" schema

  Scenario Outline: "Nft Whitelist" returns "Method Not Allowed" in case of <method> method
    Given send <method> request to "{base_url}/backend/v1/nft/invalid/whitelist" with "nft_whitelist" data
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method |
      | GET    |
      | DELETE |
      | PUT    |

  Scenario Outline: "Nft Info" returns nft info by nft ID and <contract> contract address
    Given send GET request to "{base_url}/backend/v1/nft/{chain_id}/<address>/0/info"
    Then assert response code is 200
    Then validate response by "nft_info" schema

    Examples:
      | contract | address                                    |
      | erc721   | 0xb48e6dFe1Fd8B6f1ec0DD678997B30937662F9AE |
      | erc1155  | 0xB36C2e9ed6471aC8CC2e07Cd0a5b07DfB2559dAf |

  Scenario: "Nft Info" returns error with invalid chain ID
    Given send GET request to "{base_url}/backend/v1/nft/invalid/0xb48e6dFe1Fd8B6f1ec0DD678997B30937662F9AE/0/info"
    Then assert response code is 400
    Then reason "chain ID must be valid" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Nft Info" returns error with invalid contract address
    Given send GET request to "{base_url}/backend/v1/nft/{chain_id}/invalid_address/0/info"
    Then assert response code is 400
    Then reason "contract_address: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario Outline: "Nft Info" returns "Method Not Allowed" in case of <method> method
    Given send <method> request to "{base_url}/backend/v1/nft/{chain_id}/0xb48e6dFe1Fd8B6f1ec0DD678997B30937662F9AE/0/info"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema
    Examples:
      | method |
      | POST   |
      | DELETE |
      | PUT    |