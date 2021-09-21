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
        super().__init__(names)
        logging.info("Need to override __init__() to support WSS.")
        # <Please define appium connection instance with 3P app desired capabilities here>

    def factory_reset_and_power_off(self):
        logging.info("Need to override factory_reset_and_power_off() to support WSS.")
        # <Please remove DUT within 3P app appium connection context here>
        # super().power_off()

    def power_cycle_provisioner(self):
        logging.info('No need to power cycle the provisioner for WSS device ZTS setup.')

    def power_on_and_check_setup(self):
        logging.info("Need to override power_on_and_check_setup() to support WSS.")
        # super().power_on_and_check_setup()
        # <Please check DUT from 3P app here>
