import json
import pandas as pd
from pathlib import Path
import os

from backend.services.watsonx import Watsonx

TEMPLATE_PATH = Path(__file__).parents[1] / "prompts"


class _ExplainerLLM:
    def __init__(self):
        self.llm = Watsonx("mistralai/mistral-large", stop_sequence="}")
        self.primer = """{\n\"erklärung\": \""""
        self.output_format = """{\n"erklärung": "",\n"grundstoff": "",\n"materialzusammensetzung":"",\n"kategorie": ""\n}"""

    def _get_result(self, prompt_file, context, user_input):
        prompt_path = os.path.join(TEMPLATE_PATH, prompt_file)
        llm_input = self._construct_prompt(
            prompt_file=prompt_path,
            context=context,
            output_format=self.output_format,
            user_input=user_input,
            primer=self.primer,
        )
        llm_output = self.llm.generate(llm_input)

        return self._create_json(llm_output)

    def _construct_prompt(
        self, prompt_file, output_format, context, user_input, primer
    ):
        with open(prompt_file, "r", encoding="utf-8") as file:
            prompt_template = file.read()

        filled_prompt = prompt_template.format(
            Unternehmenskontext=context,
            output_format=output_format,
            Bezeichnung=user_input,
            primer=primer,
        )

        return filled_prompt

    def _create_json(self, raw_output):
        full_output = self.primer + raw_output
        try:
            # Attempt to parse the string as JSON
            json_data = json.loads(full_output)
            return json_data  # Return the parsed JSON as a Python object
        except json.JSONDecodeError:
            # Return None or a specific message if it's not valid JSON
            return "Response was not a valid json."


class ExplainerCreator:
    def __init__(self, workload: pd.DataFrame, prompt_file: str, context: str):
        self.explainerllm = _ExplainerLLM()
        self.workload = workload
        self.prompt_file = prompt_file
        self.context = context

    def get_results(self):
        if self.workload.shape[1] == 1:
            for index, entry in self.workload.iterrows():
                response = self.explainerllm._get_result(
                    self.prompt_file, self.context, entry.values
                )
                for key, value in response.items():
                    self.workload.loc[index, key] = value
            return self.workload
        else:
            return SyntaxError
