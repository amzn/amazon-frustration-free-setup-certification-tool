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

def pytest_addoption(parser):
    """
    Parse the input arguments
    """
    parser.addoption(
        '--ffs_type',
        action='store',
        default='BSS',
        help='FFS protocol type, one of ["BSS", "ZSS"] for now'
    )
    parser.addoption(
        "--name_of_plug_to_control_dut",
        action="store",
        default='First plug',
        help='Name of the smart plug (displayed on Alexa App) to power on and off DUT'
    )
    parser.addoption(
        "--name_of_plug_to_control_provisioner",
        action="store",
        default='Second plug',
        help='Name of the smart plug (displayed on Alexa App) to power on and off provisioner device'
    )
    parser.addoption(
        "--name_of_dut",
        action="store",
        help='Name of the device under test displayed on Alexa App after the setup',
        required=True
    )
    parser.addoption(
        "--appium_server_port",
        action="store",
        default=4723,
        help='Port used to start appium server'
    )


def pytest_generate_tests(metafunc):
    """
    Convert input arguments into python test parameters
    """
    options = ['ffs_type', 'name_of_plug_to_control_dut', 'name_of_plug_to_control_provisioner', 'name_of_dut',
               'appium_server_port']
    for option in options:
        if metafunc.config.getoption(option):
            metafunc.parametrize(option, [metafunc.config.getoption(option)])
