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

from src.devices.ack_device import ACKDevice
from src.devices.bss_device import BSSDevice
from src.devices.wss_device import WSSDevice
from src.devices.zss_device import ZSSDevice
from src.appium_conn import AppiumConn

SLEEP_TIME_BETWEEN_ROUNDS_IN_SECOND = 20


def test_zts(ffs_type, name_of_plug_to_control_dut, name_of_plug_to_control_provisioner, name_of_dut, appium_server_port):
    """
    The test method defines the main test flow as below
    1. Setup Appium connection
    2. Deregister the DUT and power it off
    3. Power cycle/reboot the echo device (provisioner)
    4. Power on DUT and check the registration

    """
    device_type = {
        "ack": ACKDevice,
        "bss": BSSDevice,
        "wss": WSSDevice,
        "zss": ZSSDevice
    }
    names = [name_of_plug_to_control_dut, name_of_plug_to_control_provisioner, name_of_dut]
    device = device_type[ffs_type.lower()](names)

    AppiumConn.start_appium_server(appium_server_port)
    try:
        device.factory_reset()
        device.power_off()
        device.pre_associate_with_customer_id()
        device.power_cycle_provisioner()
        device.power_on()
        setup_time = time.time()
        device.check_device_setup()
        setup_time = time.time() - setup_time
        logging.info(f'The setup time of smart device "{name_of_dut}" is {setup_time:.2f} seconds')
    finally:
        AppiumConn.stop_appium_server()
        # Sleep some time to allow previous appium session closed properly for next round of test
        time.sleep(SLEEP_TIME_BETWEEN_ROUNDS_IN_SECOND)
