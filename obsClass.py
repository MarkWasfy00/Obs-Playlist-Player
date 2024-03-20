import obsws_python as obs
import time
import datetime
import json
import os

class OBS:
    def __init__(self) -> None:
        self.my_dict = {}
        self.current_list = [""]
        try:
            self.obs_client = obs.ReqClient(host='localhost', port=4455, password='password')
        except Exception as e:
            print(f"Error connecting to OBS: {e}")
            self.obs_client = None
        self.__load_dict()

    def __load_dict(self):
        file_path = "dictionary_data.txt"
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    serialized_data = file.read()
                    self.my_dict = json.loads(serialized_data)
        except Exception as e:
            print(f"Error loading dictionary data: {e}")

    def __save_to_dict(self):
        serialized_dict = json.dumps(self.my_dict, indent=4)
        file_path = "dictionary_data.txt"
        try:
            with open(file_path, "w") as file:
                file.write(serialized_dict)
        except Exception as e:
            print(f"Error saving dictionary data: {e}")

    def add(self, key, value):
        try:
            if key not in self.my_dict:
                self.my_dict[key] = value
                self.__save_to_dict()
        except Exception as e:
            print(f"Error adding entry to dictionary: {e}")

    def delete(self, key):
        try:
            if key in self.my_dict:
                del self.my_dict[key]
                self.__save_to_dict()
        except Exception as e:
            print(f"Error deleting entry from dictionary: {e}")

    def edit(self, key, value):
        try:
            if key in self.my_dict:
                self.my_dict[key] = value
                self.__save_to_dict()
        except Exception as e:
            print(f"Error editing entry in dictionary: {e}")

    def get(self, key):
        try:
            return self.my_dict.get(key)
        except Exception as e:
            print(f"Error getting value from dictionary: {e}")

    def go_live(self, key):
        try:
            if not self.obs_client:
                print("OBS client is not available.")
                return

            self.current_list = self.my_dict.get(key, [])
            SceneName = "my_scene"
            SourceName = "My_Video"
            scenes_list = self.obs_client.get_scene_list().scenes
            if not any(scene['sceneName'] == SceneName for scene in scenes_list):
                self.obs_client.create_scene(SceneName)
            self.obs_client.set_current_program_scene(SceneName)

            inputs_list = self.obs_client.get_input_list().inputs
            if not any(input['inputName'] == SourceName for input in inputs_list):
                Settings = {'local_file': ''}
                self.obs_client.create_input(SceneName, SourceName, 'ffmpeg_source', Settings, True)

            self.obs_client.start_stream()

            for path in self.current_list:
                full_path = os.path.abspath(os.path.join("videos", path))
                Settings = {'local_file': full_path}
                self.obs_client.set_input_settings(SourceName, Settings, True)
                time.sleep(2)
                while True:
                    if self.obs_client.get_media_input_status(SourceName).media_state == "OBS_MEDIA_STATE_ENDED":
                        break

            self.obs_client.stop_stream()
            self.obs_client.disconnect()
            print("Streaming finished.")
        except Exception as e:
            print(f"Error during live streaming: {e}")

    def schedule(self, key, startTime):
        try:
            if not self.obs_client:
                print("OBS client is not available.")
                return

            self.current_list = self.my_dict.get(key, [])
            delay = self.calculate_seconds_until(startTime)
            time.sleep(delay)
            SceneName = "my_scene"
            SourceName = "My_Video"
            scenes_list = self.obs_client.get_scene_list().scenes
            if not any(scene['sceneName'] == SceneName for scene in scenes_list):
                self.obs_client.create_scene(SceneName)
            self.obs_client.set_current_program_scene(SceneName)

            inputs_list = self.obs_client.get_input_list().inputs
            if not any(input['inputName'] == SourceName for input in inputs_list):
                Settings = {'local_file': ''}
                self.obs_client.create_input(SceneName, SourceName, 'ffmpeg_source', Settings, True)

            self.obs_client.start_stream()

            for path in self.current_list:
                full_path = os.path.abspath(os.path.join("videos", path))
                Settings = {'local_file': full_path}
                self.obs_client.set_input_settings(SourceName, Settings, True)
                time.sleep(2)
                while True:
                    if self.obs_client.get_media_input_status(SourceName).media_state == "OBS_MEDIA_STATE_ENDED":
                        break

            self.obs_client.stop_stream()
            self.obs_client.disconnect()
            print("Streaming finished.")
        except Exception as e:
            print(f"Error during scheduled streaming: {e}")

    @staticmethod
    def calculate_seconds_until(start_time):
        try:
            current_time = datetime.datetime.now()
            time_difference = start_time - current_time
            total_seconds = time_difference.total_seconds()
            return total_seconds
        except Exception as e:
            print(f"Error calculating seconds until: {e}")
            return None
