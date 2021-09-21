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


class ACKDevice(Device):

    def __init__(self, names):
        super().__init__(names)

    def factory_reset_and_power_off(self):
        logging.info("ACK device has not been supported by this certification tool yet.")

    def power_cycle_provisioner(self):
        logging.info('No need to power cycle provisioner for ACK device ZTS setup.')

    def power_on_and_check_setup(self):
        logging.info("ACK device has not been supported by this certification tool yet.")
