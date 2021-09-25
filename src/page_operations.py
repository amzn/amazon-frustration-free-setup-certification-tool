#    Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License").
#    You may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def click_element(driver, timeout, locator):
    """
    Click the element based on its locator
    :param driver: WebDriver instance to control application objects
    :param locator: XPATH locator of the element
    :param timeout: timeout to find the element
    :return: Boolean
    """
    if verify_if_element_is_present(driver, timeout, locator):
        driver.find_element(By.XPATH, locator).click()
        return True
    return False


def verify_if_element_is_present(driver, timeout, locator):
    """
    Verify if the element is visible, return false if element is always invisible within timeout
    :param driver: WebDriver instance to control application objects
    :param timeout: timeout in seconds
    :param locator: XPATH locator of the element
    :return: Boolean
    """
    try:
        WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


def verify_if_element_is_not_present(driver, timeout, locator):
    """
    Verify if the element is invisible, return false if element is always visible within timeout
    :param driver: WebDriver instance to control application objects
    :param timeout: timeout in seconds
    :param locator: XPATH locator of the element
    :return: Boolean
    """
    try:
        WebDriverWait(driver, timeout).until(expected_conditions.invisibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


def swipe_screen(driver, start_x_p, end_x_p, start_y_p, end_y_p, duration=1000):
    """
    Swipe from start point to end point
    :param driver: WebDriver instance to control application objects
    :param start_x_p: Percentage value of x-coordinate at which to start
    :param end_x_p: Percentage value of x-coordinate at which to stop
    :param start_y_p: Percentage value of y-coordinate at which to start
    :param end_y_p: Percentage value of y-coordinate at which to stop
    :param duration: time to take the swipe, in ms
    :return: None
    """
    size = driver.get_window_size()
    start_x = int(size['width'] * start_x_p)
    end_x = int(size['width'] * end_x_p)
    start_y = int(size['height'] * start_y_p)
    end_y = int(size['height'] * end_y_p)
    driver.swipe(start_x, start_y, end_x, end_y, duration)
