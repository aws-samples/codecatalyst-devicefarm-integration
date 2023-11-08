Feature: Create Task

    As a user of the Todo App,
    I want to create a task successfully,
    So that I can verify task creation functionality

    Scenario Outline: Task flow

        Given I am on the homepage of the Todo App
        When I create a task
        Then I should complete a task in the Todo app

        Examples:
        | browser_type  |
        | Chrome    |
        | Firefox       |
