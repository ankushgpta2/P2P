import openai
import yaml


class Podcast():
    def __init__(self, path_2_openai_yaml, pdf_responses):
        self.path_2_openai_yaml = path_2_openai_yaml
        self.pdf_responses = pdf_responses
        self.pod_util = PodUtility()

    def get_pod(self):
        # first get the openai API key within yaml file 
        self.pod_util.get_openai_api(
            path_2_openai_yaml=self.path_2_openai_yaml
        )

        # second get the response from the request you sent for the PDF + parse it into different sections
        print(pdf_responses[0])
        print(b)

        # third get the prompts needed for each section


        # fourth get the responses from chatGPT to form the transcript needed for the podcast 


        # fourth convert the responses into a podcast

    def parse_paper(self):
        """
        """

class PodUtility():
    def __init__(self):
        """
        """

    @staticmethod
    def get_openai_api(path_2_openai_yaml):
        # get the information from the openai yaml specified 
        with open(path_2_openai_yaml) as f:
            personal_info = yaml.load(f, Loader=SafeLoader)
            try:
                assert 'api_key' in personal_info.keys()
            except AssertionError:
                raise AssertionError(f"Missing information in .yaml file ({path_2_openai_yaml})... please reference chatgpt_info_template.yaml on required information")
        return personal_info['api_key']

    

