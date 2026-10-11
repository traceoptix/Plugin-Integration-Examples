Feature: Checkout

  Background:
    Given the bookshop catalogue is available

  @ui
  Scenario: Guest can add a book to the cart
    Given I am on the bookshop homepage
    When I search for "Clean Code"
    And I add the first result to the cart
    Then the cart badge shows 1 item

  @api
  Scenario: Cart API accepts a valid book
    Given a valid book id exists in the catalogue
    When I add the book to the cart via the API
    Then the cart API returns a 200 response
    And the response body contains the book id
