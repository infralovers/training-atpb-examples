Feature: About Page

  Scenario: Access about page
    Given I am on "the home page"
    When I follow "About"
    Then I should be on "the about page"
    And I should see "About me"

  Scenario: Return to home page
    Given I am on "the about page"
    When I follow "Back to home page"
    Then I should be on "the home page"
    And I should see "My Blog"  