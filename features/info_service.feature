@regression
Feature: Info Service
  Returns the build service info

  Scenario: Get service BACKEND version
    Returns the build service info
    Given send GET request to "{base_url}/backend/v1/version"
    Then assert response code is 200
    Then validate response by "version_info" schema

  Scenario: Get service AUTH version
    Returns the build service info
    Given send GET request to "{base_url}/auth/v1/version"
    Then assert response code is 200
    Then validate response by "version_info" schema

  Scenario: Get service EMAIL version
    Returns the build service info
    Given send GET request to "{base_url}/email/v1/version"
    Then assert response code is 200
    Then validate response by "version_info" schema

  Scenario: Get service USERS version
    Returns the build service info
    Given send GET request to "{base_url}/users/v1/version"
    Then assert response code is 200
    Then validate response by "version_info" schema