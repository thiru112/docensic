import requests
import os
import json

DOCKER_CONTAINER_TOP = "http://{}:{}/containers/{}/top"
DOCKER_CONTAINER_INSPECT = "http://{}:{}/containers/{}/json"


class Docapi():

    def __init__(self):
        self.data = ""
        self.ip = ""
        self.port = ""
        self.artifacts_path = ""
        self.executable_path = ""
        self.container_id = ""

    @staticmethod
    def chech_privilege():
        """ To check whether script is running in root privelege

        Return:
            bool: True if root, false if not
        """
        return True if (os.getuid() == 0) else False

    def load_config(self):
        """ To parse and load the config values into script
            Returns:
                bool: True if success or False if 
        """

        try:
            with open('config.json') as f:
                config = json.load(f)
        except FileNotFoundError as error_404:
            print("Rename config.json.example to config.json : ", error_404)
            return False
        except Exception as e:
            print(e)
            return False

        self.ip = config['DOCKER_API']['IP']
        self.port = config['DOCKER_API']['PORT']
        return True

    def get_container_process_info(self, container_id):
        """ To get details of the process that running inside the container
        Args:
            container_id (str): container id to be inspected
        Returns
            bool: True if successful, False otherwise.
        """
        try:
            req_url = DOCKER_CONTAINER_TOP.format(
                self.ip, self.port, container_id)
            r = requests.get(req_url)
            output = r.json()
            self.container_id = output[0]['Id']
            print(output)
        except Exception as e:
            print(e)
            return False

    def get_container_lowlevel_info(self, container_id):
        """ To get low-level information from a container

        Args:
            container_id (str): container id or name 
        Returns:
            bool: True if able to get the data, if not false
        """

        try:
            req_url = DOCKER_CONTAINER_INSPECT.format(
                self.ip, self.port, container_id)
            r = requests.get(req_url)
            print(r)
        except Exception as e:
            print(e)
            False
