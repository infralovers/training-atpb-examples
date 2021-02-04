Feature: About Page

  Feature testing about base with links from the home page to the about page
  and also backwards link to the homepage

  Scenario: Access about page

    Testing link form the home page to the about page

    Given I am on "the home page"
    When I follow "About"
    Then I should be on "the about page"
    And I should see "About me"

  Scenario: Return to home page

    Testing link from the about page to the homepage

    Given I am on "the about page"
    When I follow "Back to home page"
    Then I should be on "the home page"
    And I should see "My Blog"