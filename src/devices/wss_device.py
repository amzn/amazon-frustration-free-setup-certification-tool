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
        # TODO: define appium connection instance with 3P app desired capabilities

    def factory_reset(self):
        # TODO: within 3P app appium connection context, control the 3P app to remove DUT
        pass

    def pre_associate_with_customer_id(self):
        logging.info('Permanent pre-association must be setup for WSS device ZTS. If not, test will fail.')

    def power_cycle_provisioner(self):
        logging.info('No need to power cycle provisioner for WSS device ZTS setup.')

    def check_device_setup(self):
        super().check_device_setup()
        # TODO: check DUT from 3P app
