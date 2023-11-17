Feature: HNM Auth: Auth Service

  Scenario: "Auth Login" returns the login access token
    Given get Etherum signature
    Given send POST request to "​{base_url}/auth/v1​/auth​/login" with Etherum signature
    Then assert response code is 200
    Then validate response by "auth_login" schema

  Scenario: "Auth Login Check" checks of login exists
  Checks of login exists
    Given send GET request to "{base_url}/auth/v1/auth/login/check"
    Then assert response code is 200
    Then validate response by "login_check" schema

  Scenario: "Auth Login Check" with invalid access token
  Checks of login exists
    Given send GET request to "{base_url}/auth/v1/auth/login/check" with invalid "{invalid}" access token
    Then assert response code is 403
    Then reason "failed to get auth login" message presence in response
    Then validate response by "validation_error" schema

#  Scenario: "Auth Login Renewed" returns the renewed login info
#    Given send GET request to "{base_url}/auth/v1/auth/login/renewed"
#    Then assert response code is 200
#    Then validate response by "auth_login" schema

  Scenario: "Auth Login Renewed" returns error by not allowed method POST
    Given send POST request to "{base_url}/auth/v1/auth/login/renewed"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Auth Login Renewed" returns error by not allowed method DELETE
    Given send DELETE request to "{base_url}/auth/v1/auth/login/renewed"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Auth Login Renewed" returns error by not allowed method PUT
    Given send PUT request to "{base_url}/auth/v1/auth/login/renewed"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema