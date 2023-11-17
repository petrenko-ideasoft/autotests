Feature: HNM Auth: Challenge Service

  Scenario: Challenge Login for return the challenge info to login
    Given send POST request to "{base_url}/auth/v1/challenge/login"
    Then assert response code is 200
    Then validate response by "challenge_login" schema

  Scenario: "Challenge Login" returns error by not allowed method GET
    Given send GET request to "{base_url}/auth/v1/challenge/login"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Challenge Login" returns error by not allowed method PUT
    Given send PUT request to "{base_url}/auth/v1/challenge/login"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Challenge Login" returns error by not allowed method DELETE
    Given send DELETE request to "{base_url}/auth/v1/challenge/login"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

  Scenario: Challenge Login does not proceed challenge info to login with invalid wallet
    Given send GET request to "{base_url}/auth/v1/challenge/login" with invalid "{invalid}" wallet address
    Then assert response code is 400
    Then reason "wallet address must be valid" message presence in response
    Then validate response by "validation_error" schema
