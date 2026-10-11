Feature: Book search

  Background:
    Given the bookshop catalogue is available

  @ui
  Scenario: Search returns the matching title
    Given I am on the bookshop homepage
    When I search for "The Pragmatic Programmer"
    Then I see the book listed in the results
    And the result shows the correct author

  @ui
  Scenario: Search with no results shows a helpful message
    Given I am on the bookshop homepage
    When I search for "zzznomatchzzz"
    Then I see the empty-results message

  @api
  Scenario: API search returns results for a known title
    When I call the search API with query "Domain-Driven Design"
    Then the API response contains at least one result
    And the first result title contains "Domain-Driven Design"

  @api
  Scenario: API search with unknown query returns an empty list
    When I call the search API with query "zzznomatchzzz"
    Then the API response contains an empty results list
