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

from src.kasa_app_page_objects import KasaAppPageObjects
from src.device import *


class WSSDevice(Device):

    def __init__(self, names):
        super().__init__(names)
        self.kasa_app_desired_caps = {
            "platformName": "Android",
            "deviceName": "Android",
            "appPackage": "com.tplink.kasa_android",
            "appActivity": "com.tplink.hellotp.activity.SplashScreenActivity",
            "newCommandTimeout": 0,
            "noReset": True,
            "udid": get_phone_uuid(),
            "automationName": "UiAutomator2"
        }
        self.kasa_app = AppiumConn(self.kasa_app_desired_caps)

    def factory_reset(self):
        with self.kasa_app.appium_conn_context() as driver:
            kasa_pages = KasaAppPageObjects(driver, self.names[2])
            kasa_pages.remove_dut()

    def pre_associate_with_customer_id(self):
        logging.info('Permanent pre-association must be setup for WSS device ZTS. If not, test will fail.')

    def power_cycle_provisioner(self):
        logging.info('No need to power cycle provisioner for WSS device ZTS setup.')

    def check_device_setup(self):
        # Check dut on Alexa App
        super().check_device_setup()

        # Check dut on Kasa App
        with self.kasa_app.appium_conn_context() as driver:
            kasa_pages = KasaAppPageObjects(driver, self.names[2])
            kasa_pages.wait_until_smart_dut_present(SLEEP_TIME_WAIT_FOR_SMART_DUT_PRESENT_IN_SECOND)