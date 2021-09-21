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

import json
import logging
import subprocess
import sys
import time
from contextlib import contextmanager
from appium.webdriver import Remote

SLEEP_TIME_BEFORE_APPIUM_CLIENT_CONNECT_IN_SECOND = 20


def get_phone_uuid():
    """
    Retrieve UUID of connected android phone via adb command
    :return: String
    """
    getprop_cmd = f'adb shell getprop ro.serialno'.split()
    proc = subprocess.Popen(getprop_cmd, stdout=subprocess.PIPE)
    uuid = proc.communicate()[0].decode("utf-8").strip()
    return uuid


class AppiumConn:
    """
    This class is used to define an object to control Alexa app on mobile device
    """
    port = 4723

    def __init__(self, capabilities):
        """
        Initialize the AppiumConn object
        :param capabilities: Desired capabilities of mobile device
        """
        self.caps = capabilities
        self.driver = None

    @staticmethod
    def stop_appium_server():
        """
        Quit and Kill Appium server process
        """
        try:
            if sys.platform == 'win32':
                cleanup_cmd = 'taskkill /f /im node.exe /t'.split()
            elif sys.platform == 'darwin':
                cleanup_cmd = 'killall node'.split()
            elif sys.platform == 'linux':
                cleanup_cmd = 'killall node'.split()
            else:
                cleanup_cmd = ''
            subprocess.Popen(cleanup_cmd)
            logging.info(f'Killed Appium Node')
        except Exception as e:
            logging.exception(f'Failed to Kill Appium Server: {e.args}')
            raise

    @staticmethod
    def start_appium_server(server_port):
        """
        Start appium service locally
        """
        if sys.platform == 'win32':
            appium_cmd = 'appium.cmd'
        else:
            appium_cmd = 'appium'

        AppiumConn.port = server_port
        start_cmd = f'{appium_cmd} -p {AppiumConn.port} --log logs/appium_server_log.txt'.split()
        subprocess.Popen(start_cmd)
        logging.info('Appium Server is up')
        time.sleep(SLEEP_TIME_BEFORE_APPIUM_CLIENT_CONNECT_IN_SECOND)

    def start_appium_client(self, ext_appium_server_url):
        """
        Start appium client with desired capabilities to control mobile app
        """
        if ext_appium_server_url:
            url = ext_appium_server_url
        else:
            url = f'http://localhost:{AppiumConn.port}/wd/hub'
        self.driver = Remote(url, self.caps, keep_alive=True)

        app_capabilities = json.dumps(self.caps)
        logging.info(f'Appium Client is ready with capacities {app_capabilities}')

    @contextmanager
    def appium_conn_context(self, ext_appium_server_url=None):
        """
        Define a context for operations on appium controlled app
        """
        try:
            self.start_appium_client(ext_appium_server_url)
            yield self.driver
        except Exception as e:
            logging.error(f'{type(e).__name__}:{e.args}')
            raise
        finally:
            if self.driver:
                self.driver.quit()
