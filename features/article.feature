Feature: Article

  Scenario: Creating a new Article
    Given I have a healthy API
    When I create an article with the title "Python is awesome"
    Then I should receive a "success" response
    And I should receive "Python is awesome" in the response body

  Scenario Outline:
    Given I have a healthy API
    When I create an article with the title "<title>" and content "<content>"
    Then I should receive a "success" response
    And I should receive "<title>" in the response body
    And I should receive "<content>" in the response body

    Examples:
      | title | content |
      | this is test content one | my content number one |
      | this is test content 2 | and another test content |

  Scenario: Listing all articles
       Given I have a healthy API
       When I list all available articles
       Then I should receive a "success" response
       And I should receive "Python is awesome" in the response body