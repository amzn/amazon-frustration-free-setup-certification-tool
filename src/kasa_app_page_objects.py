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

import time
from src.page_operations import *

"""
Locator for Android Kasa App
There are main types of selector can be used to find elements, By.XPATH is used here
Ref: https://github.com/appium/appium-desktop#the-appium-desktop-inspector
"""

SMART_DEVICE_LOCATOR_TEMP = '//android.widget.TextView[@text="NAME"]'
SMART_DEVICE_CONFIG_LOCATOR = '//android.widget.ImageView[@resource-id="com.tplink.kasa_android:id' \
                              '/image_nav_action_icon"]'
REMOVE_DEVICE_LOCATOR = '//android.widget.FrameLayout[@resource-id="com.tplink.kasa_android:id' \
                              '/button_delete_device"]'
REMOVE_DEVICE_TITLE_LOCATOR = '//android.widget.TextView[@text="Remove Smart Plug"]'

# Number of swipe in order to find smart device from your all devices list, adjust it if required
NUM_OF_SWIPE_TO_FIND_DEVICE = 2


class KasaAppPageObjects:
    """
    The class is used to define the operations against Kasa App page objects
    """

    def __init__(self, driver, dut_name):
        """
        Initialize the AlexaAppPageObjects object
        :param driver: WebDriver instance to control application page objects
        :param dut_name: Name of DUT
        """
        self.driver = driver
        self.dut_name = dut_name
        self.smart_dut = SMART_DEVICE_LOCATOR_TEMP.replace('NAME', self.dut_name)

    def click_smart_dut_from_devices_page(self, times):
        logging.info(f'[Kasa App] Clicking smart device "{self.dut_name}"')
        for _ in range(times):
            if click_element(self.driver, 10, self.smart_dut):
                return
            else:
                swipe_screen(self.driver, 0.50, 0.50, 0.70, 0.30)
        assert click_element(self.driver, 10, self.smart_dut), \
            f'Cannot click on smart device "{self.dut_name}".'

    def click_settings_from_smart_device_page(self):
        logging.info('[Kasa App] Clicking the settings icon')
        assert click_element(self.driver, 10, SMART_DEVICE_CONFIG_LOCATOR), 'Cannot click the settings icon'

    def click_remove_device_from_device_settings_page(self):
        logging.info('[Kasa App] Clicking "Remove Device" button')
        assert click_element(self.driver, 10, REMOVE_DEVICE_LOCATOR), 'Cannot click the "Remove Device" button'

    def click_remove_device_from_remove_device_page(self):
        if verify_if_element_is_present(self.driver, 10, REMOVE_DEVICE_TITLE_LOCATOR):
            logging.info('[Kasa App] Clicking "Remove Device" button to confirm')
            assert click_element(self.driver, 10, REMOVE_DEVICE_LOCATOR), 'Cannot click "DELETE" button'
        else:
            assert False, '"Remove Device" page does not present'

    def is_smart_dut_present(self):
        logging.info(f'[Kasa App] Checking smart device "{self.dut_name}"')
        swipe_screen(self.driver, 0.50, 0.50, 0.30, 0.70)
        return verify_if_element_is_present(self.driver, 10, self.smart_dut)

    def wait_until_smart_dut_present(self, timeout):
        time_start = time.time()
        time_stop = time_start + timeout
        while time.time() < time_stop:
            if self.is_smart_dut_present():
                return
            time.sleep(1)
        assert False, f'The smart device "{self.dut_name}" not found within {timeout/60} minutes'

    def remove_dut(self):
        # Deregister dut
        smart_dut_found = True
        try:
            self.click_smart_dut_from_devices_page(NUM_OF_SWIPE_TO_FIND_DEVICE)
        except AssertionError:
            smart_dut_found = False
            logging.info(f'[Kasa App] Smart device "{self.dut_name}" not found in Devices page')

        if smart_dut_found:
            self.click_settings_from_smart_device_page()
            self.click_remove_device_from_device_settings_page()
            self.click_remove_device_from_remove_device_page()
