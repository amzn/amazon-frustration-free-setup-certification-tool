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

from src.device import *


class WSSDevice(Device):

    def __init__(self, names):
        logging.info("Need to override __init__() to support WSS.")
        super().__init__(names)
        # Please define appium connection instance with 3P app desired capabilities here and take the example below
        # as reference.
        '''
        self.3p_app_desired_caps = {
            "platformName": "Android",
            "deviceName": "Android",
            "appPackage": "<package name of your application>",
            "appActivity": "<class name of your application's launcher activity>",
            "newCommandTimeout": 0,
            "noReset": True,
            "udid": get_phone_uuid(),
            "automationName": "UiAutomator2"
        }
        
        self.3p_app = AppiumConn(self.3p_app_desired_caps)
        '''

    def factory_reset_and_power_off(self):
        logging.info("Need to override factory_reset_and_power_off() to support WSS.")
        # First, please remove DUT within your app's appium connection context here and you can take the
        # template/pseudocode below as reference. You could write a class to remove device action and define all related
        # page objects (take delete_dut() from alexa_app_page_objects.py as reference); super().names[2] is the name of
        # DUT displayed on both Alexa App and 3P app by default.
        '''
        # with self.3p_app.appium_conn_context() as driver:
            3p_app_pages = <your_app_page_objects_class>(driver, super().names[2])
            3p_app_pages.remove_dut()
        '''
        # Second, please call power_off() from device.py to turn off the DUT as below.
        '''
        super().power_off()
        '''

    def power_cycle_provisioner(self):
        logging.info('No need to power cycle the provisioner for WSS device ZTS setup.')

    def power_on_and_check_setup(self):
        logging.info("Need to override power_on_and_check_setup() to support WSS.")
        # First, please call power_on_and_check_setup() from device.py to turn on the DUT and check it from Alexa App.
        '''
        super().power_on_and_check_setup()
        '''
        # Second, please also check the visibility of DUT on your app within your app's appium connection context here
        # and you can take the template/pseudocode below as reference. You could write a class to keep checking device
        # status until either that device is found or a predefined timeout (5 minutes here) and define all related page
        # objects (take wait_until_smart_dut_present() from alexa_app_page_objects.py as reference); super().names[2]
        # is the name of DUT displayed on both Alexa App and 3P app by default.
        '''
        # with self.3p_app.appium_conn_context() as driver:
            3p_app_pages = <your_app_page_objects_class>(driver, super().self.names[2])
            3p_app_pages.wait_until_smart_dut_present(SLEEP_TIME_WAIT_FOR_SMART_DUT_PRESENT_IN_SECOND)
        '''
