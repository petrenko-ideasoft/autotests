@regression @users
Feature: HNM Users
  Returns the build service info

  Scenario: Get user info
  Returns the user info
    Given send GET request to "{base_url}/users/v1/user"
    Then assert response code is 200
    Then validate response by "user_info" schema

  Scenario: Get user info by invalid wallet address
  Returns the user info
    Given send GET request to "{base_url}/users/v1/user" with invalid "{random}" wallet
    Then assert response code is 400
    Then reason "wallet_address: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "User Email Change" returns info about update user's email
    Given post "{user_email_def}" email for user using ""{base_url}/users/v1/user/email"

  Scenario: "User Locale" returns info about user's locale
  Returns the user info
    Given send GET request to "{base_url}/users/v1/user/locale"
    Then assert response code is 200
    Then validate response by "user_locale_info" schema

  Scenario Outline: "User Locale" returns "Method Not Allowed" in case of
    Given send <method_name> request to "{base_url}/users/v1/user/locale"
    Then assert response code is 200
    Then reason "Method Not Allowed" message presence in response
    Then validate response by "validation_error" schema

    Examples:
      | method_name |
      | POST        |
      | DELETE      |

  Scenario: "User Locale Change" returns info about edit user's locale
    Given send PUT request to "{base_url}/users/v1/user/locale" with "en" locale
    Then assert response code is 200
    Then validate response by "user_locale_info" schema

  Scenario: "User Locale Change" returns error if invalid user's locale is sent
    Given send PUT request to "{base_url}/users/v1/user/locale" with "invalid" locale
    Then assert response code is 400
    Then reason "locale: the length must be exactly 2." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "User Locale Change" returns error if no locale is sent for user's locale
    Given send PUT request to "{base_url}/users/v1/user/locale"
    Then assert response code is 400
    Then reason "locale: cannot be blank." message presence in response
    Then validate response by "validation_error" schema

