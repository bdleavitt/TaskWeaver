import os
from openai import AzureOpenAI
from taskweaver.plugin import Plugin, register_plugin


@register_plugin
class UtilConvertPluginCodeToYaml(Plugin):
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
                "content": "You are an AI assistant that takes a python class written for use  as a taskweaver plugin and generate the corresponding YAML file that contains the description and other metadata.\n\nReturn only the YAML output wihtout any additional comment. \n\nYou must return properly formatted YAML with proper indents. \n\nIn the schema, there are several fields that should be filled, including name, enabled, required, description, parameters and returns. "
            },
            {
                "role": "user",
                "content": "from taskweaver.plugin import Plugin, register_plugin\n\n\n@register_plugin\nclass TellJoke(Plugin):\n    def __call__(self, lan: str = \"en\"):\n        try:\n            import pyjokes\n        except ImportError:\n            raise ImportError(\"Please install pyjokes first.\")\n\n        # Define the API endpoint and parameters\n        return pyjokes.get_joke(language=lan, category=\"neutral\")"
            },
            {
                "role": "assistant",
                "content": "name: tell_joke\nenabled: true\nrequired: false\nplugin_only: true\ndescription: >-\n  Call this plugin to tell a joke.\nexamples: |-\n  result = tell_joke(\"en\")\n\nparameters:\n  - name: lan\n    type: str\n    required: false\n    description: the language of the joke. Default is English. It can be en, de, es, it, gl, eu.\n\n\nreturns:\n  - name: joke\n    type: str\n    description: the joke."
            }
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