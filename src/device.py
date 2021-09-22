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

import logging
import time
from src.appium_conn import get_phone_uuid, AppiumConn
from src.alexa_app_page_objects import AlexaAppPageObjects

# Timeouts
SLEEP_TIME_WAIT_FOR_PROVISIONER_IN_SECOND = 60
SLEEP_TIME_WAIT_FOR_SMART_DUT_PRESENT_IN_SECOND = 300


class Device:

    def __init__(self, names):
        self.names = names
        self.alexa_app_desired_caps = {
            "platformName": "Android",
            "deviceName": "Android",
            "appPackage": "com.amazon.dee.app",
            "appActivity": "com.amazon.dee.app.Launcher",
            "newCommandTimeout": 0,
            "noReset": True,
            "udid": get_phone_uuid(),
            "automationName": "UiAutomator2"
        }
        self.alexa_app = AppiumConn(self.alexa_app_desired_caps)

    def factory_reset(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.delete_dut()

    def power_off(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.power_off_dut()

    def factory_reset_and_power_off(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.delete_dut()
            alexa_pages.power_off_dut()

    def power_cycle_provisioner(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.power_off_and_on_provisioner()
        time.sleep(SLEEP_TIME_WAIT_FOR_PROVISIONER_IN_SECOND)

    def power_on_and_check_setup(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.power_on_dut()
            setup_time = time.time()
            alexa_pages.click_navigate_back_from_plug_device_page()
            alexa_pages.wait_until_smart_dut_present(SLEEP_TIME_WAIT_FOR_SMART_DUT_PRESENT_IN_SECOND)
            setup_time = time.time() - setup_time
            logging.info(f'The setup time of smart device "{self.names[2]}" is {setup_time:.2f} seconds')
