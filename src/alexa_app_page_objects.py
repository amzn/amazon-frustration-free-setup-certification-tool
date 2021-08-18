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
from src.page_operations import *

"""
Locator for Android Alexa App
There are main types of selector can be used to find elements, By.XPATH is used here
Ref: https://github.com/appium/appium-desktop#the-appium-desktop-inspector
"""
DEVICES_LOCATOR = '//android.widget.LinearLayout[@content-desc="Tab, Devices"]'
DEVICES_PAGE_TITLE = '//android.view.View[@text="DEVICES"]'
ALL_DEVICES_LOCATOR = '//android.widget.Button[@content-desc="All Devices"]'
SMART_DEVICE_LOCATOR_TEMP = '//android.widget.TextView[@text="NAME"]'
SMART_DEVICE_TITLE_LOCATOR_TEMP = '//android.view.View[@text="NAME"]'
SMART_DEVICE_CONFIG_LOCATOR = '//android.widget.Button[@content-desc="Edit"]'
SMART_DEVICE_DELETE_LOCATOR = '//android.widget.Button[@content-desc="Delete"]'
SMART_DEVICE_DELETE_CONFIRM_LOCATOR = '//android.widget.Button[@text="DELETE"]'
SMART_DEVICE_UNRESPONSIVE = '//android.widget.TextView[@text="Device is unresponsive"]'
PLUG_DEVICE_POWER_ON_LOCATOR = '//android.widget.Switch[@text="on"]'
PLUG_DEVICE_POWER_OFF_LOCATOR = '//android.widget.Switch[@text="off"]'

# Number of swipe in order to find smart device from your all devices list, adjust it if required
NUM_OF_SWIPE_TO_FIND_DEVICE = 2

# Timeouts
SLEEP_TIME_BEFORE_PROVISIONER_POWER_ON_IN_SECOND = 20


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

    def click_devices_from_home_page(self):
        logging.info('[Alexa App] Clicking "Devices" button')
        assert click_element(self.driver, 10, DEVICES_LOCATOR), 'Cannot click on "Devices" button'

    def is_smart_device_responsive(self):
        logging.info('[Alexa App] Checking "Device is unresponsive" message')
        if verify_if_element_is_present(self.driver, 30, self.smart_dut_title):
            if verify_if_element_is_not_present(self.driver, 30, SMART_DEVICE_UNRESPONSIVE):
                return
        assert False, f'[Alexa App] Smart device "{self.device_names[2]}" not responsive, ' \
                      f'please do factory reset manually'

    def swipe_and_click_all_devices(self):
        swipe_screen(self.driver, 0.70, 0.30, 0.17, 0.17)
        logging.info('[Alexa App] Clicking "All Devices" button')
        assert click_element(self.driver, 10, ALL_DEVICES_LOCATOR), 'Cannot click on "All Devices"'

    def click_smart_device_from_all_devices_page(self, smart_device, times=10):
        m = re.search('@text="([\\w|\\s]+)"', smart_device)
        name_of_smart_device = m.group(1)
        logging.info(f'[Alexa App] Clicking smart device "{name_of_smart_device}"')
        for _ in range(times):
            if click_element(self.driver, 10, smart_device):
                return
            else:
                swipe_screen(self.driver, 0.50, 0.50, 0.70, 0.30)
        assert click_element(self.driver, 10, smart_device), \
            f'Cannot click on smart device "{name_of_smart_device}".'

    def click_settings_from_smart_device_page(self):
        logging.info('[Alexa App] Clicking the settings icon')
        assert click_element(self.driver, 10, SMART_DEVICE_CONFIG_LOCATOR), 'Cannot click the settings icon'

    def click_delete_from_smart_device_config_page(self):
        logging.info('[Alexa App] Clicking the delete icon')
        assert click_element(self.driver, 10, SMART_DEVICE_DELETE_LOCATOR), 'Cannot click the delete icon'

    def click_delete_confirm_from_smart_device_config_page(self):
        logging.info('[Alexa App] Clicking "DELETE" button to confirm')
        assert click_element(self.driver, 10, SMART_DEVICE_DELETE_CONFIRM_LOCATOR), 'Cannot click "DELETE" button'

    def click_power_off_from_plug_device_page(self):
        logging.info('[Alexa App] Clicking the power icon to turn it off')
        assert click_element(self.driver, 10, PLUG_DEVICE_POWER_ON_LOCATOR), 'Cannot click the power icon'
        assert verify_if_element_is_present(self.driver, 10, PLUG_DEVICE_POWER_OFF_LOCATOR), \
            'Cannot switch to power off'

    def click_power_on_from_plug_device_page(self):
        logging.info('[Alexa App] Clicking the power icon to turn it on')
        assert click_element(self.driver, 10, PLUG_DEVICE_POWER_OFF_LOCATOR), 'Cannot click the power icon'
        assert verify_if_element_is_present(self.driver, 10, PLUG_DEVICE_POWER_ON_LOCATOR), 'Cannot switch to power on'

    def is_smart_dut_present(self):
        logging.info(f'[Alexa App] Checking smart device "{self.device_names[2]}"')
        swipe_screen(self.driver, 0.50, 0.50, 0.30, 0.70)
        return verify_if_element_is_present(self.driver, 10, self.smart_dut)

    def wait_until_smart_dut_present(self, timeout):
        time_start = time.time()
        time_stop = time_start + timeout
        while time.time() < time_stop:
            if self.is_smart_dut_present():
                return
            time.sleep(1)
        assert False, f'The smart device "{self.device_names[2]}" not found within {timeout/60} minutes'

    def move_to_all_devices_page(self):
        self.click_devices_from_home_page()
        self.swipe_and_click_all_devices()

    def delete_dut(self):
        # Deregister DUT by deleting it from configuration page
        smart_dut_found = True
        try:
            self.click_smart_device_from_all_devices_page(self.smart_dut, NUM_OF_SWIPE_TO_FIND_DEVICE)
        except AssertionError:
            smart_dut_found = False
            logging.info(f'[Alexa App] Smart device "{self.device_names[2]}" not found in all devices page')

        if smart_dut_found:
            # Check whether it's responsive
            self.is_smart_device_responsive()
            self.click_settings_from_smart_device_page()
            self.click_delete_from_smart_device_config_page()
            self.click_delete_confirm_from_smart_device_config_page()

    def power_off_dut(self):
        self.click_smart_device_from_all_devices_page(self.smart_plug_of_dut, NUM_OF_SWIPE_TO_FIND_DEVICE)
        try:
            self.click_power_off_from_plug_device_page()
        except AssertionError:
            logging.info(f'Plug device "{self.device_names[0]}" is in power off mode')

    def power_cycle_provisioner(self):
        self.click_smart_device_from_all_devices_page(self.smart_plug_of_provisioner, NUM_OF_SWIPE_TO_FIND_DEVICE)
        try:
            self.click_power_off_from_plug_device_page()
            time.sleep(SLEEP_TIME_BEFORE_PROVISIONER_POWER_ON_IN_SECOND)
        except AssertionError:
            logging.info(f'Plug device "{self.device_names[1]}" is in power off mode')
        self.click_power_on_from_plug_device_page()

    def power_on_dut(self):
        self.click_smart_device_from_all_devices_page(self.smart_plug_of_dut, NUM_OF_SWIPE_TO_FIND_DEVICE)
        self.click_power_on_from_plug_device_page()
