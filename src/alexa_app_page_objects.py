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

import re
import time
import logging

from selenium.common.exceptions import NoSuchElementException
from src.page_operations import *

"""
Locator for Android Alexa App
There are main types of selector can be used to find elements, By.XPATH is used here
Ref: https://github.com/appium/appium-desktop#the-appium-desktop-inspector
"""
DEVICES_LOCATOR = '//android.widget.LinearLayout[@content-desc="Tab, Devices"]'
DEVICES_PAGE_TITLE = '//android.view.View[@text="DEVICES"]'
ALL_DEVICES_LOCATOR = '//android.widget.Button[@content-desc="All Devices"]'
ALL_DEVICES_PAGE_TITLE = '//android.view.View[@text="ALL DEVICES"]'
SMART_DEVICE_LOCATOR_TEMP = '//android.widget.TextView[@text="NAME"]'
SMART_DEVICE_TITLE_LOCATOR_TEMP = '//android.view.View[@text="NAME"]'
SMART_DEVICE_CONFIG_LOCATOR = '//android.widget.Button[@content-desc="Edit"]'
SMART_DEVICE_DELETE_LOCATOR = '//android.widget.Button[@content-desc="Delete"]'
SMART_DEVICE_DELETE_CONFIRM_LOCATOR = '//android.widget.Button[@text="DELETE"]'
SMART_DEVICE_UNRESPONSIVE = '//android.widget.TextView[@text="Device is unresponsive"]'
PLUG_DEVICE_POWER_ON_LOCATOR = '//android.widget.Switch[@text="on"]'
PLUG_DEVICE_POWER_OFF_LOCATOR = '//android.widget.Switch[@text="off"]'
PLUG_DEVICE_BACK_LOCATOR = '//android.widget.Button[@content-desc="Back"]'
DEVICE_TYPE_ICONS_Horizontal_ScrollView_CLASS_NAME = 'android.widget.HorizontalScrollView'
ALL_DEVICES_ScrollView_CLASS_NAME = 'android.widget.ScrollView'

MAX_SWIPES_OF_SCROLL_TO_END = 5

# Timeouts
SLEEP_TIME_BEFORE_PROVISIONER_POWER_ON_IN_SECOND = 10
TIMEOUT_MEDIUM = 10
TIMEOUT_SMALL = 2


class AlexaAppPageObjects:
    """
    The class is used to define the operations against Alexa App page objects
    """

    def __init__(self, driver, device_names):
        """
        Initialize the AlexaAppPageObjects object
        :param driver: WebDriver instance to control application page objects
        :param device_names: Name of DUT and plugs to control DUT and provisioner
        """
        self.driver = driver
        self.device_names = device_names
        self.smart_plug_of_dut = SMART_DEVICE_LOCATOR_TEMP.replace('NAME', self.device_names[0])
        self.smart_plug_of_provisioner = SMART_DEVICE_LOCATOR_TEMP.replace('NAME', self.device_names[1])
        self.smart_dut = SMART_DEVICE_LOCATOR_TEMP.replace('NAME', self.device_names[2])
        self.smart_dut_title = SMART_DEVICE_TITLE_LOCATOR_TEMP.replace('NAME', self.device_names[2].upper())

    def click_devices_from_home_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking "Devices" button')
        assert click_element(self.driver, timeout, DEVICES_LOCATOR), 'Cannot click on "Devices" button'

    # DUT might not be responsive, then removing the device from Alexa App might not factory reset it and a hard reset
    # is needed. This is the checking to halt the execution in that case.
    def is_smart_device_responsive(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Checking "Device is unresponsive" message')
        if verify_if_element_is_present(self.driver, timeout, self.smart_dut_title):
            if verify_if_element_is_not_present(self.driver, timeout, SMART_DEVICE_UNRESPONSIVE):
                return
        assert False, f'[Alexa App] Smart device "{self.device_names[2]}" not responsive, ' \
                      f'please do factory reset manually'

    def is_on_devices_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Checking whether it is on device page')
        return verify_if_element_is_present(self.driver, timeout, DEVICES_PAGE_TITLE)

    def is_on_all_devices_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Checking whether it is on ALL Devices page')
        return verify_if_element_is_present(self.driver, timeout, ALL_DEVICES_PAGE_TITLE)

    def swipe_and_click_all_devices(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Swiping devices buttons to the right end to show "All Devices" button')
        self.driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().className("' + DEVICE_TYPE_ICONS_Horizontal_ScrollView_CLASS_NAME +
            '").instance(0)).setAsHorizontalList().scrollToEnd(' + str(MAX_SWIPES_OF_SCROLL_TO_END) + ');')
        logging.info('[Alexa App] Clicking "All Devices" button')
        assert click_element(self.driver, timeout, ALL_DEVICES_LOCATOR), 'Cannot click on "All Devices"'

    def click_smart_device_from_all_devices_page(self, smart_device, timeout=TIMEOUT_MEDIUM):
        m = re.search('@text="([\\w|\\s]+)"', smart_device)
        name_of_smart_device = m.group(1)
        logging.info(f'[Alexa App] Searching and clicking smart device "{name_of_smart_device}"')
        self.driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().className("' + ALL_DEVICES_ScrollView_CLASS_NAME + '").instance(0))'
            '.scrollIntoView(new UiSelector().text("' + name_of_smart_device + '").instance(0));')
        assert click_element(self.driver, timeout, smart_device), \
            f'Cannot click on smart device "{name_of_smart_device}".'

    def click_settings_from_smart_device_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking the settings icon')
        assert click_element(self.driver, timeout, SMART_DEVICE_CONFIG_LOCATOR), 'Cannot click the settings icon'

    def click_delete_from_smart_device_config_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking the delete icon')
        assert click_element(self.driver, timeout, SMART_DEVICE_DELETE_LOCATOR), 'Cannot click the delete icon'

    def click_delete_confirm_from_smart_device_config_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking "DELETE" button to confirm')
        assert click_element(self.driver, timeout, SMART_DEVICE_DELETE_CONFIRM_LOCATOR), 'Cannot click "DELETE" button'

    def click_power_off_from_plug_device_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking the power icon to turn it off')
        assert click_element(self.driver, timeout, PLUG_DEVICE_POWER_ON_LOCATOR), 'Cannot click the power icon'
        assert verify_if_element_is_present(self.driver, timeout, PLUG_DEVICE_POWER_OFF_LOCATOR), \
            'Cannot switch to power off'

    def click_power_on_from_plug_device_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking the power icon to turn it on')
        assert click_element(self.driver, timeout, PLUG_DEVICE_POWER_OFF_LOCATOR), 'Cannot click the power icon'
        assert verify_if_element_is_present(self.driver, timeout, PLUG_DEVICE_POWER_ON_LOCATOR), \
            'Cannot switch to power on'

    def is_smart_dut_present(self, timeout=TIMEOUT_SMALL):
        logging.info(f'[Alexa App] Refreshing screen and checking smart device "{self.device_names[2]}"')
        # Swipe the screen to refresh all devices page
        swipe_screen(self.driver, start_x_p=0.50, end_x_p=0.50, start_y_p=0.30, end_y_p=0.70)
        return verify_if_element_is_present(self.driver, timeout, self.smart_dut)

    def wait_until_smart_dut_present(self, timeout):
        time_start = time.time()
        time_stop = time_start + timeout
        while time.time() < time_stop:
            if self.is_smart_dut_present():
                return
        assert False, f'The smart device "{self.device_names[2]}" not found within {timeout/60} minutes'

    def move_to_all_devices_page(self):
        self.click_devices_from_home_page()

        if self.is_on_devices_page():
            self.swipe_and_click_all_devices()

    def delete_dut(self):
        # Deregister DUT by deleting it from configuration page
        smart_dut_found = True
        try:
            self.click_smart_device_from_all_devices_page(self.smart_dut)
        except (NoSuchElementException, AssertionError):
            smart_dut_found = False
            logging.info(f'[Alexa App] Smart device "{self.device_names[2]}" not found in all devices page')

        if smart_dut_found:
            # Check whether it's responsive
            self.is_smart_device_responsive()
            self.click_settings_from_smart_device_page()
            self.click_delete_from_smart_device_config_page()
            self.click_delete_confirm_from_smart_device_config_page()

    def power_off_dut(self):
        if not self.is_on_all_devices_page(timeout=TIMEOUT_SMALL) and self.is_on_devices_page(timeout=TIMEOUT_SMALL):
            self.swipe_and_click_all_devices()

        self.click_smart_device_from_all_devices_page(self.smart_plug_of_dut)
        try:
            self.click_power_off_from_plug_device_page()
        except AssertionError:
            logging.info(f'Plug device "{self.device_names[0]}" is in power off mode')

    def power_off_and_on_provisioner(self):
        self.click_smart_device_from_all_devices_page(self.smart_plug_of_provisioner)
        try:
            self.click_power_off_from_plug_device_page()
            time.sleep(SLEEP_TIME_BEFORE_PROVISIONER_POWER_ON_IN_SECOND)
        except AssertionError:
            logging.info(f'Plug device "{self.device_names[1]}" is in power off mode')
        self.click_power_on_from_plug_device_page()

    def power_on_dut(self):
        self.click_smart_device_from_all_devices_page(self.smart_plug_of_dut)
        self.click_power_on_from_plug_device_page()

    def click_navigate_back_from_plug_device_page(self, timeout=TIMEOUT_MEDIUM):
        logging.info('[Alexa App] Clicking the navigate back icon')
        assert click_element(self.driver, timeout, PLUG_DEVICE_BACK_LOCATOR), 'Cannot click the navigate back icon'
        assert self.is_on_all_devices_page(), 'Cannot navigate to "ALL DEVICES" page'
