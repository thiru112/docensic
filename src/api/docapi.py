#!/usr/bin/python3
import requests
import os
import json

DOCKER_CONTAINER_TOP = "http://{}:{}/containers/{}/top"
DOCKER_CONTAINER_INSPECT = "http://{}:{}/containers/{}/json"
DOCKER_CONTAINER_FILE_SYSTEM_CHANGES = "http://{}:{}/containers/{}/changes"
DOCKER_CONTIANER_LOGS = "http://{}:{}/containers/{}/logs?stdout=true&stderr=true&timestamps=true"
DOCKER_CONTAINER_EXPORT = "http://{}:{}/containers/{}/export"
DOCKER_CONTAINER_COMMIT = "http://{}:{}/commit?container={}&repo=Forensic&tag=copy&author=investigation_copy&pause=true"
DOCKER_IMAGE_INFO = "http://{}:{}/images/{}/json"
DOCKER_IMAGE_HISTORY = "http://{}:{}/images/{}/history"
DOCKER_EXEC_INSPECT = "http://{}:{}/exec/{}/json"
DOCKER_NETWORK_INSPECT = "http://{}:{}/networks/{}"
DOCKER_CONTAINER_LIST = "http://{}:{}/containers/json"
DOCKER_CONTAINER_EXTRACT_DATA = "http://{}:{}/containers/{}/archive?path={}"


class Docapi():

    def __init__(self):
        self.data = ""
        self.ip = ""
        self.port = ""
        self.artifacts_path = ""
        self.tar_path = ""
        self.container_id = ""
        self.image_id = ""
        self.exec_id = ""
        self.network_id = ""
        self.mount_points = []
        self.volume_path = ""

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
        self.artifacts_path = config['ARTIFACTS']['BASE_PATH']
        self.tar_path = config['ARTIFACTS']['TAR_PATH']
        self.volume_path = config['ARTIFACTS']['VOLUME_DATA_PATH']
        return True

    def get_container_process_info(self):
        """ To get details of the process that running inside the container

        Returns
            bool: True if successful, False otherwise.
        """
        try:
            req_url = DOCKER_CONTAINER_TOP.format(
                self.ip, self.port, self.container_id)
            r = requests.get(req_url)
            output = r.json()
            self.save_as_json_file("container_process_info", output)
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
            output = r.json()
            self.container_id = output['Id']
            self.exec_id = output['ExecIDs']
            self.network_id = list(output['NetworkSettings']['Networks'])
            self.artifacts_path = self.artifacts_path.format(self.container_id)
            self.tar_path = self.tar_path.replace(
                'BASE_PATH', self.artifacts_path)
            self.volume_path = self.volume_path.replace(
                'BASE_PATH', self.artifacts_path)
            all_mount_points = output['Mounts']
            for i in all_mount_points:
                self.mount_points.append(i['Destination'])
            self.mkdir()
            self.save_as_json_file("container_low_level_inspect", output)
        except Exception as e:
            print(e)
            return False
        return True

    def get_container_file_system_changes(self):
        """ To know what are the files that are changed in container filesystem

        Return:
            bool: True if info is extracted, otherwise false
        """
        try:
            req = DOCKER_CONTAINER_FILE_SYSTEM_CHANGES.format(
                self.ip, self.port, self.container_id)
            r = requests.get(req)
            output = r.json()
            self.save_as_json_file("container_file_sytem_changes", output)
        except Exception as e:
            print(e)
            return False

        return True

    def get_container_logs(self):
        """ To get container logs

        Return:
            bool: True if success, else false
        """
        try:
            req = DOCKER_CONTIANER_LOGS.format(
                self.ip, self.port, self.container_id)
            r = requests.get(req)
            output = r.text
            log_complete_path = self.artifacts_path + '/container_log_data.log'
            try:
                with open(log_complete_path, 'w') as logwr:
                    logwr.write(output)
            except FileExistsError as fe:
                print(fe)
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def export_container_as_tarball(self):
        """ To get container as tarball image

        Return:
            bool: True if success, else false
        """
        try:
            req = DOCKER_CONTAINER_EXPORT.format(
                self.ip, self.port, self.container_id)
            r = requests.get(req, stream=True)
            tar_path_to_write = self.tar_path + '/' + "container_complete.tar"
            if r.status_code == 200:
                try:
                    with open(tar_path_to_write, 'wb') as tar:
                        tar.write(r.raw.read())
                except FileExistsError as fe:
                    print(fe)
        except Exception as e:
            print(e)
            return False
        return True

    def container_to_image_commit(self):
        """ To commit a running container image

        Return:
            bool: True if success, else false
        """

        try:
            req = DOCKER_CONTAINER_COMMIT.format(
                self.ip, self.port, self.container_id)
            r = requests.post(req)
            output = r.json()
            print(output)
        except Exception as e:
            print(e)
            return False
        return True

    def get_image_corresponding_container(self):
        """ To get image info  for the corresponding container_id

        Return:
            bool: True if success, else false
        """

        try:
            req = DOCKER_IMAGE_INFO.format(self.ip, self.port, self.image_id)
            r = requests.get(req)
            output = r.json()
            self.save_as_json_file("image_details_of_the_container", output)
        except Exception as e:
            print(e)

    def get_image_history(self):
        """ To get the commands given in the corresponding image information,
            such as commands in the image

        Return:
            bool: True if success, else false
        """

        try:
            req = DOCKER_IMAGE_HISTORY.format(
                self.ip, self.port, self.image_id)
            r = requests.get(req)
            output = r.json()
            self.save_as_json_file("image_history", output)
        except Exception as e:
            print(e)
            return False
        return True

    def get_exec_info_for_contianer(self):
        """ To get the exec instance associated with the container

        Return:
            bool: True if success, else false        
        """

        try:
            if self.exec_id is not None:
                for exec_ids in self.exec_id:
                    req = DOCKER_EXEC_INSPECT.format(
                        self.ip, self.port, exec_ids)
                    r = requests.get(req)
                    output = r.json()
                    self.save_as_json_file("exec_session_list", output)
        except Exception as e:
            print(e)
            return False

        return True

    def get_network_details(self):
        """ To get network details corresponding a container

        Return:
            bool: True is success, else false
        """

        try:
            if self.network_id is not None:
                for network_ids in self.network_id:
                    req = DOCKER_NETWORK_INSPECT.format(
                        self.ip, self.port, network_ids)
                    r = requests.get(req)
                    output = r.json()
                    self.save_as_json_file("container_network_details", output)
        except Exception as e:
            print(e)
            return False
        return True

    def extract_volume_data(self):
        """ To extract all the volume data, passwd that are in the container

        Returns:
            bool: True if able to extract data, false otherwise
        """
        try:
            if self.mount_points is not None:
                for i in self.mount_points:
                    req = DOCKER_CONTAINER_EXTRACT_DATA.format(
                        self.ip, self.port, self.container_id, i)
                    r = requests.get(req, stream=True)
                    tar_path = self.volume_path + '/' + \
                        i.replace('/', '_') + '.tar'
                    if r.status_code == 200:
                        try:
                            with open(tar_path, 'wb') as tf:
                                tf.write(r.raw.read())
                        except FileExistsError as fe:
                            print(fe)
        except Exception as e:
            print(e)
            return False
        return True

    def mkdir(self):
        """ To create directories to store the artifacts for each containers and subfolders

        Return:
            bool: True is success, else false
        """
        try:
            for path in [self.artifacts_path, self.tar_path, self.volume_path]:
                if not os.path.exists(path):
                    try:
                        os.makedirs(path, mode=0o700)
                    except FileExistsError as e:
                        print("Directory already exists:", e)
        except Exception as e:
            print(e)
            return False

        return True

    def save_as_json_file(self, file_name, file_contents):
        """ To save the output in json file format for further investigation

        Parameter:
            file_name: string - Gets file name that need to be created
            file_contents: json - Contents that need to be stored in the file
        Returns:
            bool: True if able to create file, else false
        """
        file_name_complete_path = self.artifacts_path + '/' + file_name + '.json'
        try:
            with open(file_name_complete_path, 'w') as fi:
                json.dump(file_contents, fi, indent=4)
        except FileExistsError as fe:
            print("The file exists ", fe)
            return False
        except Exception as e:
            print(e)
            return False
        return True

    def list_containers(self):
        """ To list all the container that are running the system
        Return:

        """
        try:
            req = DOCKER_CONTAINER_LIST.format(self.ip, self.port)
            r = requests.get(req)
            output = r.json()
            print("Container ID\t Container Name")
            print("------------     --------------")
            for container_id in output:
                print(container_id['Id'][:12], "\t",
                      container_id['Names'][0][1:])
        except Exception as e:
            print(e)
