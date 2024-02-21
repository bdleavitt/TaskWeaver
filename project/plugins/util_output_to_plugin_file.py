import os  
from typing import Optional  
from taskweaver.plugin import Plugin, register_plugin  
  
@register_plugin  
class UtilOutputToPluginFile(Plugin):  
    def __call__(self, plugin_name: str, code_string: str, file_type: str)-> tuple[str, str]:  
        """  
        Writes an input string to a file in the specified directory.  
          
        Parameters:  
        plugin_name (str): The name of the plugin / file to be created.  
        code_string (str): The string to write to the file.  
        file_type (str): The type of the file. Must be either 'py' or 'yaml'.  
          
        Returns:  
        str: The path to the written file.  
          
        Raises:  
        ValueError: If `file_type` is not 'py' or 'yaml'.  
        """   
  
        ## get the project path from the environment variable
        project_path = os.getenv("PROJECT_DIRECTORY_PATH")

        ## create a plugins_draft directory if it does not exist
        draft_dir = os.path.join(project_path, "plugins_draft")
        if not os.path.exists(draft_dir):
            os.makedirs(draft_dir)

        
        if file_type not in ['py', 'yaml']:  
            raise ValueError("file_type must be either 'py' or 'yaml'")  
    
        file_path = os.path.join(draft_dir, f"{plugin_name}.{file_type}")  
  
        with open(file_path, 'w') as f:  
            f.write(code_string)  
          
        description = f"File {plugin_name}.{file_type} has been written to {draft_dir}."  
        return file_path, description  