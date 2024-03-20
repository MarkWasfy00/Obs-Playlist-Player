import obsws_python as obs
import time
import datetime
import json

class OBS ():
    def __init__(self) -> None:
        
        self.my_dict = {}
        self.current_list=[""]
    
    def __load_dict(self):
        file_path = "dictionary_data.txt"
        with open(file_path, "r") as file:
            serialized_data = file.read()

        # Deserialize JSON to dictionary
        self.my_dict = json.loads(serialized_data)



    def __save_to_dict(self):
        serialized_dict = json.dumps(self.my_dict, indent=4)  # indent for pretty formatting

        # Step 3: Write the serialized data to a file, clearing old data if any
        file_path = "dictionary_data.txt"
        with open(file_path, "w") as file:
            file.write(serialized_dict)

        print("Dictionary saved to:", file_path)

    def add(self,key,value):
        self.__load_dict()
        key_to_add = key
        if key_to_add in self.my_dict:
            pass
        else:
            self.my_dict[key]=value
            self.__save_to_dict()


    def delete(self,key):
        self.__load_dict()
        if key in self.my_dict:
            del self.my_dict[key]
            self.__save_to_dict()
        else:
            pass


    def edit(self,key,value):
        self.__load_dict()
        if key in self.my_dict:
            self.my_dict[key]=value
            self.__save_to_dict()
        else:
            pass        


    def get(self,key):
        self.__load_dict()
        if key in self.my_dict:
            return(self.my_dict[key])
    
    

    def go_live(self,key):
        self.current_list=self.my_dict[key]
        #--------------------------------------------------------------------------------------------------------------------------intialize the names of the scene and media source
        SceneName="my_scene"
        SourceName="My_Video"
        #--------------------------------------------------------------------------------------------------------------------------connect to OBS   
        cl = obs.ReqClient(host='localhost', port=4455, password='password') 
        #--------------------------------------------------------------------------------------------------------------------------Creating the SCENE and check if there is a scene already with the same name
        
        scenes_list=cl.get_scene_list()
        found=0
        for scene_dict in scenes_list.scenes:
            if scene_dict['sceneName'] == SceneName:
                found=1
            else:
                pass
        if (found==0):
            cl.create_scene(SceneName)

        cl.set_current_program_scene(SceneName)
        #---------------------------------------------------------------------------------------------------------------------------creating a media source and check if there is a media source already wiht the same name 
        inputs_list=cl.get_input_list()
        found=0
        for input_dict in inputs_list.inputs:
            if input_dict['inputName'] == SourceName:
                found=1
            else:
                pass
        if (found==0):
            
            Settings={'local_file':''}
            cl.create_input(SceneName,SourceName,'ffmpeg_source',Settings,True)
        #--------------------------------------------------------------------------------------------------------------------------starting stream after transform of the window
        itemId=cl.get_scene_item_id(scene_name=SceneName,source_name=SourceName).scene_item_id
        resizeValue={'alignment': 5, 'boundsAlignment': 0, 'boundsHeight': 1.0, 'boundsType': 'OBS_BOUNDS_NONE', 'boundsWidth': 1.0, 'cropBottom': 0, 'cropLeft': 0, 'cropRight': 0, 'cropTop': 0, 'height': 720.0, 'positionX': 0.0, 'positionY': 0.0, 'rotation': 0.0, 'scaleX': 1.5, 'scaleY': 1.5, 'sourceHeight': 720.0, 'sourceWidth': 1000.0, 'width': 1000.0}
        cl.set_scene_item_transform(scene_name=SceneName,item_id=itemId,transform=resizeValue)  
        cl.start_stream()
        for path in self.current_list:
            Settings={'local_file': 'videos/'+path}
        
            cl.set_input_settings(SourceName,Settings,True)
            time.sleep(2)
            while(True):
                if(cl.get_media_input_status(SourceName).media_state =="OBS_MEDIA_STATE_ENDED" ): 
                    break
        #--------------------------------------------------------------------------------------------------------------------------# ###Stop streaming in OBS (optional)
        cl.stop_stream()
        #--------------------------------------------------------------------------------------------------------------------------# ### Disconnect from OBS
        cl.disconnect()
        #--------------------------------------------------------------------------------------------------------------------------
        print("Streaming finished.")  
    def schedule(self,key,startTime):
        self.current_list=self.my_dict[key]
        #--------------------------------------------------------------------------------------------------------------------------calculate the delay time
        theDelay=self.calculate_seconds_until(startTime)
        time.sleep(theDelay)
        #--------------------------------------------------------------------------------------------------------------------------intialize the names of the scene and media source
        SceneName="my_scene"
        SourceName="My_Video"
        #--------------------------------------------------------------------------------------------------------------------------connect to OBS   
        cl = obs.ReqClient(host='localhost', port=4455, password='password') 
        #--------------------------------------------------------------------------------------------------------------------------Creating the SCENE and check if there is a scene already with the same name
        
        scenes_list=cl.get_scene_list()
        found=0
        for scene_dict in scenes_list.scenes:
            if scene_dict['sceneName'] == SceneName:
                found=1
            else:
                pass
        if (found==0):
            cl.create_scene(SceneName)

        cl.set_current_program_scene(SceneName)
        #---------------------------------------------------------------------------------------------------------------------------creating a media source and check if there is a media source already wiht the same name 
        inputs_list=cl.get_input_list()
        found=0
        for input_dict in inputs_list.inputs:
            if input_dict['inputName'] == SourceName:
                found=1
            else:
                pass
        if (found==0):
            
            Settings={'local_file':''}
            cl.create_input(SceneName,SourceName,'ffmpeg_source',Settings,True)
        #--------------------------------------------------------------------------------------------------------------------------
        itemId=cl.get_scene_item_id(scene_name=SceneName,source_name=SourceName).scene_item_id
        resizeValue={'alignment': 5, 'boundsAlignment': 0, 'boundsHeight': 1.0, 'boundsType': 'OBS_BOUNDS_NONE', 'boundsWidth': 1.0, 'cropBottom': 0, 'cropLeft': 0, 'cropRight': 0, 'cropTop': 0, 'height': 720.0, 'positionX': 0.0, 'positionY': 0.0, 'rotation': 0.0, 'scaleX': 1.5, 'scaleY': 1.5, 'sourceHeight': 720.0, 'sourceWidth': 1000.0, 'width': 1000.0}
        cl.set_scene_item_transform(scene_name=SceneName,item_id=itemId,transform=resizeValue)  
        cl.start_stream()
        for path in self.current_list:
            Settings={'local_file':'videos/'+path}
            cl.set_input_settings(SourceName,Settings,True)
            time.sleep(2)
            while(True):
                if(cl.get_media_input_status(SourceName).media_state =="OBS_MEDIA_STATE_ENDED" ): 
                    break
        #--------------------------------------------------------------------------------------------------------------------------# ###Stop streaming in OBS (optional)
        cl.stop_stream()
        #--------------------------------------------------------------------------------------------------------------------------# ### Disconnect from OBS
        cl.disconnect()
        #--------------------------------------------------------------------------------------------------------------------------
        print("Streaming finished.")        

    def calculate_seconds_until(start_time):
        # Get current datetime
        current_time = datetime.datetime.now()
        
        # Calculate the difference between start time and current time
        time_difference = start_time - current_time
        
        # Convert time difference to total seconds
        total_seconds = time_difference.total_seconds()
        
        return total_seconds
    



