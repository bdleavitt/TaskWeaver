import os
from openai import AzureOpenAI
from taskweaver.plugin import Plugin, register_plugin


@register_plugin
class UtilConvertPythonToPlugin(Plugin):
    def __call__(self, python_code: str) -> str:
        # Note: The openai-python library support for Azure OpenAI is in preview.
        # Note: This code sample requires OpenAI Python library version 1.0.0 or higher.

        if type(python_code) == str:
            python_code_string = python_code
        else:
            python_code_string = str(python_code)

        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-15-preview",
        )

        open_ai_model_deployment = os.getenv("OPEN_AI_DEPLOYMENT_NAME")

        messages = [
            {
                "role": "system",
                "content": 'You are an AI assistant that takes a python function and converts it into a Taskweaver plugin. \n\nTaskweaver plugins are python classes that can be called by the taskweaver AI framework. \n\nfrom taskweaver.plugin import Plugin, register_plugin\n\n@register_plugin\nclass PluginTemplate(Plugin):\n    def __call__(self, *args, **kwargs):\n        """Implementation Starts"""\n        result, description = YourImplementation()\n        """Implementation Ends"""\n\n        # if your want to add artifact from the execution result, uncomment the following code\n        # self.ctx.add_artifact(\n        #     name="artifact",\n        #     file_name="artifact.csv",\n        #     type="df",\n        #     val=result,\n        # )\n        return result, description\n\nThe typical way of implementing the plugin is to change the code between Implementation Starts and Implementation Ends. Note that the return are two variables result and description. The result stores whatever output required for follow-up processing (e.g., a DataFrame). The description is a string to describe the result.\n\nReturn only the requested python code with no additional commentary. Use proper formatting and indentation, including any pep8 formatting concerns. Maintain or add the docstring if it is missing. ',
            },
            {
                "role": "user",
                "content": "import pandas as pd\nfrom typing import Union\nfrom taskweaver.plugin import Plugin, register_plugin\n\n\ndef test_negative_income(self, df: pd.DataFrame) -> pd.DataFrame:\n    \"\"\"\n    Filter a DataFrame for entries where 'GrossBase' is less than 0.\n\n    Parameters:\n    df (pd.DataFrame): The DataFrame containing the dividend income report data.\n\n    Returns:\n    pd.DataFrame: A DataFrame containing only the entries with 'GrossBase' < 0.\n    \"\"\"\n    if not isinstance(df, pd.DataFrame):\n        raise ValueError('Input must be a pandas DataFrame.')\n\n    # Check if 'GrossBase' column exists in the DataFrame\n    if 'GrossBase' not in df.columns:\n        raise ValueError(\"DataFrame must contain a 'GrossBase' column.\")\n\n    # Filter the DataFrame for entries where 'GrossBase' < 0\n    filtered_df = df[df['GrossBase'] < 0]\n    return filtered_df\n\n# Example usage:\n# df = pd.DataFrame(...)  # Your DataFrame with data\n# filtered_results = filter_negative_gross_base_df(df)\n# print(filtered_results)\n",
            },
            {
                "role": "assistant",
                "content": "import pandas as pd\nfrom typing import Union\nfrom taskweaver.plugin import Plugin, register_plugin\n\n@register_plugin\nclass TestNegativeIncome(Plugin):\n    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:\n        \"\"\"\n        Filter a DataFrame for entries where 'GrossBase' is less than 0.\n\n        Parameters:\n        df (pd.DataFrame): The DataFrame containing the dividend income report data.\n\n        Returns:\n        pd.DataFrame: A DataFrame containing only the entries with 'GrossBase' < 0.\n        \"\"\"\n        if not isinstance(df, pd.DataFrame):\n            raise ValueError('Input must be a pandas DataFrame.')\n\n        # Check if 'GrossBase' column exists in the DataFrame\n        if 'GrossBase' not in df.columns:\n            raise ValueError(\"DataFrame must contain a 'GrossBase' column.\")\n\n        # Filter the DataFrame for entries where 'GrossBase' < 0\n        filtered_df = df[df['GrossBase'] < 0]\n        return filtered_df\n\n    # Example usage:\n    # df = pd.DataFrame(...)  # Your DataFrame with data\n    # filtered_results = filter_negative_gross_base_df(df)\n    # print(filtered_results)\n",
            },
        ]

        messages.append(
            {"role": "user", "content": python_code_string}
        )

        try: 
            completion = client.chat.completions.create(
                model=open_ai_model_deployment,  # model = "deployment_name"
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            response = completion.choices[0].message.content

        except Exception as e:
            print(f"An error occurred while creating the completion: {e}")
        return response