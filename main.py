#!/usr/bin/python3.9

import requests
from bs4 import BeautifulSoup
import os
import warnings 
import argparse

# import in the pdf related functions
from get_pdfs import *

# import in the text message related function
from notify_via_text import send_text

# import in the podcast related function
from convert_2_podcast import *


def get_args():
    parser = argparse.ArgumentParser(description="Parameters For WebScraper")
    parser.add_argument('--url', type=str, default='https://paperswithcode.com', help='the url to the website to scrape')
    parser.add_argument('--send_text_message', type=bool, default=True, help='whether or not to send text message')
    parser.add_argument('--convert_to_podcast', type=bool, default=True, help='whether or not to convert to podcast')
    parser.add_argument('--name_of_text_yaml', type=str, default='ankush_text_info.yaml', help='name of yaml file for text')
    parser.add_argument('--name_of_openai_yaml', type=str, default='ankush_chatgpt_info.yaml', help='name of yaml file for chatgpt')
    return parser


def main():
    # get user arguments
    args = get_args().parse_args()
    parameters = vars(args)

    # define certain variables
    parameters['page'] = requests.get(parameters['url'])
    parameters['soup'] = BeautifulSoup(parameters['page'].content, "html.parser")

    # instantiate instance of the text retrieval class
    get_text = TextRetrieval(parameters)

    # gets the pdf file
    get_text.get_pdf()

    # sends the text message if you decided to do so 
    if parameters['send_text_message'] is True and get_text.for_text_message:

        # first get absolute path to the yaml file
        base_dir = get_base_dir(__file__)
        path_2_text_yaml = f"{base_dir}/text_configs/{parameters['name_of_text_yaml']}"

        send_text(
            paper_information=get_text.for_text_message,
            path_2_text_yaml=path_2_text_yaml
        )

    # convert to a podcast if you decide to do so
    if parameters['convert_to_podcast'] is True and get_text.pdf_responses:

        # get the absolute path to the yaml file
        base_dir = get_base_dir(__file__)
        path_2_openai_yaml = f"{base_dir}/openai_configs/{parameters['name_of_openai_yaml']}"

        # instantiate class instance 
        podcast = Podcast(
            path_2_openai_yaml=path_2_openai_yaml,
            pdf_responses=get_text.pdf_responses
        )

        # call the main class function for getting the podcast 
        podcast.get_pod()

get_base_dir = lambda file_path: '/'.join(file_path.split('/')[:-1])


if __name__ == "__main__":
    main()




