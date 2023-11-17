@regression
Feature: HNM Email Templates
  Validation of Email templates route

#  CreateTemplate
  Scenario: "Create Template" returns the info about create new template
    Given post a new email template "{base_url}/email/v1/template"
    Then assert response code is 200
    Then validate response by "new_email_template" schema

  Scenario: "Create Template" returns "Status Forbidden" with invalid authorization token
    Given post a new email template "{base_url}/email/v1//v1/template" with invalid authorization "invalid" token
    Then assert response code is 403
    Then reason "failed to get auth login" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Create Template" returns error with duplicated template name
    Given post a new email template "{base_url}/email/v1/template"
    And post a new email template with the same name using "{base_url}/email/v1/template"
    Then assert response code is 400
    Then reason "the name for specified the language must be unique" message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Create Template" returns an error with empty name
    Given post a new email template "{base_url}/email/v1/template" with next data
    """
    {
        "name": "",
        "language": "en"
    }
    """
    Then assert response code is 400
    Then reason "name: cannot be blank." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Create Template" returns an error with empty language
    Given post a new email template "{base_url}/email/v1/template" with next data
    """
    {
        "name": "no language",
        "language": ""
    }
    """
    Then assert response code is 400
    Then reason "language: cannot be blank." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Create Template" returns an error with invalid language
    Given post a new email template "{base_url}/email/v1/template" with next data
    """
    {
        "name": "invalid language",
        "language": "asd"
    }
    """
    Then assert response code is 400
    Then reason "language: value must be valid." message presence in response
    Then validate response by "validation_error" schema

#  TemplateBulkRemove
#  Scenario: TemplateBulkRemove returns the info about bulk remove templates by IDs
#    Given send GET request to "{base_url}/backend/v1/review/nft/prepare/challenge"
#    Then assert response code is 200
#    Then validate response by "nft_prepare_challenge" schema

  # TemplateListByNam
  Scenario: "Template List By Name" returns the template list by name
    Given post a new email template "{base_url}/email/v1/template"
    And get email template list by "{template_name}" name using "{base_url}/email/v1/template/by/name/list"
    Then assert response code is 200
    Then validate response by "template_by_list_name" schema

  Scenario: "Template List By Name" returns error with 0 limit
    Given post a new email template "{base_url}/email/v1/template"
    And get email template list by with 0 limit using "{base_url}/email/v1/template/by/name/list"
    Then assert response code is 400
    Then reason "limit: cannot be blank." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Template List By Name" returns error with blank name
    Given post a new email template "{base_url}/email/v1/template"
    And get email template list by "blank" name using "{base_url}/email/v1/template/by/name/list"
    Then assert response code is 400
    Then reason "name: cannot be blank." message presence in response
    Then validate response by "validation_error" schema

#  TemplateCloneByIDToLang
  Scenario Outline: "Template Clone By ID To Lang" returns the info about clone template by ID to  lang
    Given post a new email template "{base_url}/email/v1/template"
    And clone email "{template_id}" template for "<language>" language using "{base_url}/email/v1/template/clone/{source_template_id}/to/<language>/lang"
    Then assert response code is 200
    Then validate response by "template_clone" schema

    Examples:
      | language |
      | ar       |

#  TemplateLanguagesList
  Scenario: "Template Languages List" returns the languages list of templates
    Given get languages list of templates by "{base_url}/email/v1/template/languages/list"
    Then assert response code is 200
    Then validate response by "template_languages_list" schema

#  TemplateListByLang
  Scenario Outline: "Template List By Lang" returns the template list by language
    Given get languages list of templates for "<language>" language by "{base_url}/email/v1/template/<language>/list"
    Then assert response code is 200
    Then validate response by "template_by_language_list" schema

    Examples:
      | language |
      | en       |

  Scenario: "Template List By Lang" returns error by incorrect language
    Given get languages list of templates for "<language>" language by "{base_url}/email/v1/template/ln/list"
    Then assert response code is 400
    Then reason "language: value must be valid." message presence in response
    Then validate response by "validation_error" schema

  Scenario: "Template List By Lang" returns error with invalid authorization token
    Given get languages list of templates for "en" language by "{base_url}/email/v1/template/ln/list" with invalid authorization "invalid" token
    Then assert response code is 403
    Then reason "failed to get auth login" message presence in response
    Then validate response by "validation_error" schema

#  TemplateByID
  Scenario: "Template By ID" returns the info about template by ID
    Given post a new email template "{base_url}/email/v1/template"
    And get info email template using "{base_url}/email/v1/template/{template_id}" by ID
    Then assert response code is 200
    Then validate response by "template_info" schema

  Scenario: "Template By ID" returns error by invalid ID
    And get info email template using "{base_url}/email/v1/template/invalid" by ID
    Then assert response code is 400
    Then reason "template_id: must be a valid UUID." message presence in response
    Then validate response by "validation_error" schema

#  UpdateTemplateByID
  Scenario: "Update Template By ID" returns the info about update template by ID
    Given post a new email template "{base_url}/email/v1/template"
    And update email template using "{base_url}/email/v1/template/{template_id}" by ID
    Then assert response code is 200

  Scenario: "Update Template By ID" returns error by invalid template ID
    And update email template using "{base_url}/email/v1/template/invalid" by ID
    Then assert response code is 400
    Then reason "template_id: must be a valid UUID." message presence in response
    Then validate response by "validation_error" schema