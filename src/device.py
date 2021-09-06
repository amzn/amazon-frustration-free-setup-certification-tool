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
from abc import abstractmethod

from src.appium_conn import get_phone_uuid, AppiumConn
from src.alexa_app_page_objects import AlexaAppPageObjects

# Number of swipe in order to find smart device from your all devices list, adjust it if required
NUM_OF_SWIPE_TO_FIND_DEVICE = 2

# Timeouts
SLEEP_TIME_WAIT_FOR_PROVISIONER_IN_SECOND = 60
SLEEP_TIME_WAIT_FOR_MANUALLY_PRE_ASSOCIATION_IN_SECOND = 120
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

    @abstractmethod
    def pre_associate_with_customer_id(self):
        raise NotImplementedError()

    def power_cycle_provisioner(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.power_cycle_provisioner()
        time.sleep(SLEEP_TIME_WAIT_FOR_PROVISIONER_IN_SECOND)

    def power_on(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.power_on_dut()

    def check_device_setup(self):
        with self.alexa_app.appium_conn_context() as driver:
            alexa_pages = AlexaAppPageObjects(driver, self.names)
            alexa_pages.move_to_all_devices_page()
            alexa_pages.wait_until_smart_dut_present(SLEEP_TIME_WAIT_FOR_SMART_DUT_PRESENT_IN_SECOND)