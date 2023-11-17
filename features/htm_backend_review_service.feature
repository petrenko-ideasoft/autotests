@regression @review
Feature: HNM Backend Review Service
  Verification os the backend review service

  Scenario: "Create Minting Nft Review" creates the review of nft for internal smart "erc1155" contract
  Generates the review NFT ID for smart "erc1155" contract
    Given send POST request to "{base_url}/backend/v1/minting/nft/review" with "nft_contract_erc1155" data
    Then assert response code is 200
    Then validate response by "get_review_id" schema

  Scenario: "Create Minting Nft Review" creates the review of nft for internal smart "erc721" contract
  Generates the review NFT ID for smart "erc721" contract
    Given send POST request to "{base_url}/backend/v1/minting/nft/review" with "nft_contract_erc721" data
    Then assert response code is 200
    Then validate response by "get_review_id" schema


  Scenario Outline: "Create Minting Nft Review" returns an error by using invalid smart contract
  Generates the review NFT ID for smart "erc721" contract
    Given send POST request to "{base_url}/backend/v1/minting/nft/review" with "nft_contract_<request_data>" data
    Then assert response code is 400
    Then reason "<error_message>" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | request_data     | error_message                             |
      | empty_contract   | contract_address: cannot be blank.        |
      | invalid_contract | contract_address: must be a valid value.  |
      | zero_copies      | number_of_copies: must be no less than 1. |
      | empty_royalty    | royalty_percent: cannot be blank.         |
      | empty_token      | token_uri: cannot be blank.               |
      | empty_signature  | eip721_signature: cannot be blank.        |


#  SendReviewNftMessageByID

  Scenario: "Preparing Of Challenge For Review Nft" preparing challenge for review nft
    Given send GET request to "{base_url}/backend/v1/review/nft/prepare/challenge"
    Then assert response code is 200
    Then validate response by "nft_prepare_challenge" schema

  Scenario: "Review Items List" returns list with review requests
    Given send POST request to "{base_url}/backend/v1/review/request/list" with "pending_review_requests" data
    Then assert response code is 200
    Then validate response by "list_with_review_requests" schema

  Scenario: "Review Item By ID" returns info about review request by ID
    Given send POST request to "{base_url}/backend/v1/minting/nft/review" with "nft_contract_erc1155" data
    And send GET request to "{base_url}/backend/v1/review/request/{review_id}"
    Then assert response code is 200
    Then validate response by "review_nft_info" schema

  Scenario Outline: "Review Item By ID" returns error in case of invalid "<review_id>" review ID
    And send GET request to "{base_url}/backend/v1/review/request/<review_id>"
    Then assert response code is 400
    Then reason "<message>" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | review_id | message                            |
      | 00000     | review_id: must be no less than 1. |
      | lorem     | review_id: value must be valid.    |

  Scenario Outline: "Review Item By ID" returns "Method Not Allowed" in case of <method> method
    Given send POST request to "{base_url}/backend/v1/minting/nft/review" with "nft_contract_erc1155" data
#    Given send POST request to "{base_url}/backend/v1/minting/nft/review"
    And send <method> request to "{base_url}/backend/v1/review/request/{review_id}"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method |
      | POST   |
      | DELETE |
      | PUT    |

#  ReviewRequestMessagesList
#/v1/review/request/{review_id}/messages/list
