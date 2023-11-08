import logging
import pytest
import traceback
import os
import time
import uuid
from pathlib import Path

from pytest_bdd import scenario, given, when, then, parsers
from hamcrest import assert_that, equal_to, contains_string

from selenium.webdriver.chrome.options import Options as chrome_options_mod
from selenium.webdriver.firefox.options import Options as firefox_options_mod

from selenium import webdriver

from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TODO_APP_URL = os.environ["TEST_URL"]
TASK_GUID = uuid.uuid4()
GRID_URL = os.environ["GRID_URL"]


def wait_until_loaded(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

current_dir = Path(__file__).resolve().parent.parent

@scenario(f"{current_dir}/features/todo.feature", "Task flow")
def test_scenario_outline():
    pass

@pytest.fixture
def context():
    class Context(object):
        pass

    return Context()


@pytest.fixture
def init_driver(request):
    
    if request._pyfuncitem.callspec.id == "Chrome":
      options = chrome_options_mod()
    else:
      options = firefox_options_mod()
    
    b = Remote(command_executor=GRID_URL, options=options,)

    b.implicitly_wait(10)
    yield b
    b.quit()


@given(parsers.parse("I am on the homepage of the Todo App"))
def goto_homepage(init_driver):
    try:
        init_driver.get(TODO_APP_URL)
        browser_title = init_driver.title
        assert_that(browser_title, equal_to("Todo App"))
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        raise (err)


@when("I create a task")
def create_task(init_driver):
    try:
        create_todo_button = wait_until_loaded(
            init_driver, '//*[@id="create-new-button"]'
        )
        create_todo_button.click()
        time.sleep(2)
        item_name_box = wait_until_loaded(
            init_driver, '//*[contains(@aria-labelledby, "formField12")]'
        )
        item_name_box.send_keys(f"MyTask {TASK_GUID}")

        item_description_box = wait_until_loaded(
            init_driver, '//*[contains(@aria-labelledby, "formField13")]'
        )
        item_description_box.send_keys(
            "My description - this is a really important task that you must complete"
        )

        submit_todo_button = wait_until_loaded(init_driver, '//*[@id="submit-button"]')
        submit_todo_button.click()

    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        raise (err)


@then("I should complete a task in the Todo app")
def check_task_exists(init_driver):
    try:
        # Should complete a task
        time.sleep(5)
        init_driver.get(TODO_APP_URL)

        task_create_result = wait_until_loaded(
            init_driver, f'//a[text()="MyTask {TASK_GUID}"]/ancestor::div[4]//button'
        )

        assert_that(task_create_result.text, contains_string("Mark as complete"))

        task_create_result.click()

        time.sleep(2)

        # Should complete a task within 10s
        complete_result = WebDriverWait(init_driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f'//a[text()="MyTask {TASK_GUID}"]/ancestor::div[4]//span[text()="Completed"]',
                )
            )
        )
        assert_that(complete_result.text, contains_string("Completed"))
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        raise (err)
