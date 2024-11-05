import os
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams


class Watsonx:
    def __init__(self, model_id, stop_sequence: str):
        load_dotenv()

        self.URL = os.environ["URL"]
        self.API_KEY = os.environ["API_KEY"]
        self.PROJECT_ID = os.environ["PROJECT_ID"]
        self.MODEL_ID = model_id

        # To display example params enter
        GenParams().get_example_values()

        direct_generate_params = {
            GenParams.STOP_SEQUENCES: [f"{stop_sequence}"],
            GenParams.REPETITION_PENALTY: 1.05,
            GenParams.MAX_NEW_TOKENS: 400,
        }

        self.model_inference = ModelInference(
            model_id=self.MODEL_ID,
            params=direct_generate_params,
            credentials=Credentials(
                api_key=self.API_KEY,
                url=self.URL,
            ),
            project_id=self.PROJECT_ID,
        )

    def generate(self, prompt_text):
        return self.model_inference.generate_text(prompt_text)
