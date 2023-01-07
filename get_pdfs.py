from notify_via_text import send_text
import requests
from bs4 import BeautifulSoup
import os
import warnings 
from datetime import date
import glob
today = date.today()


class TextRetrieval():
    def __init__(self, parameters):
        self.parameters = parameters
        self.base_path = '/'.join(__file__.split('/')[:-1])
        self.download_location = f"{self.base_path}/paperswithcode/{today.strftime('%b_%d_%Y')}"
        self.for_text_message = {}
        self.global_iterator = 0
        self.splitted = None
        self.pdf_responses = []
    
    def get_pdf(self):
        self.splitted = [x.split('"/')[1].split('">')[0] for x in str(self.parameters['soup']).split("\n") 
                    if '<a href="/paper/' in x  # conditional 1
                    and '<h1>' not in x  # conditional 2
                    and '#' not in x  # conditional 3
        ]

        for substring in self.splitted:
            nested_url = f"{self.parameters['url']}/{substring}"
            paper_name = substring.split('/')[-1]
            # get the pdf link + response 
            response = self.get_pdf_link(
                nested_url=nested_url, 
                paper_name=paper_name
            )

            # call the utility function for actually reading the PDF in 
            self.download_pdf(response, paper_name, nested_url)
        
        if self.global_iterator == 0:
            warnings.warn(f"\n\nWARNING: Did not download any PDFs... most likely because they already exist! Please double check.")
        else:
            print(f"\nDownloaded {self.global_iterator}/{len(self.splitted)} Papers that Were Found")

    def get_pdf_link(self, nested_url, paper_name):
        # get all of the hyperlinks
        response = requests.get(nested_url)
        nested_soup = BeautifulSoup(response.text, 'html.parser')
        self.hyperlinks = nested_soup.find_all('a')

        # loop through the hyperlinks and figure out if it is for a pdf
        i = 0
        for link in self.hyperlinks:
            if '.pdf' in link.get('href', []):
                # Get response object for link
                response = requests.get(link.get('href'))
        return response 

    def download_pdf(self, response, paper_name, nested_url):
        # check if the paper exists in any of the other directories
        feedback = self.check_if_paper_exists(
            paper_name=paper_name
        )

        if feedback is False:
            # check that download location exists
            if not os.path.exists(f"{self.download_location}"):
                os.makedirs(f"{self.download_location}", exist_ok=True)
            
            # make a new pdf in this location
            if not os.path.isfile(f"{self.download_location}/{paper_name}.pdf"):
                print("Downloading Paper: ", paper_name)
                pdf = open(f"{self.download_location}/{paper_name}.pdf", 'wb')
                pdf.write(response.content)
                pdf.close()

                # update certain values + print out stuff 
                print(f"File Downloaded!\n")
                self.global_iterator += 1

                # assert that it exists 
                if not os.path.isfile(f"{self.download_location}/{paper_name}.pdf"):
                    raise ValueError(f"Following file was not properly downloaded despite not being found: {self.download_location}/{paper_name}.pdf")

                # update the information for text message
                self.for_text_message[str(paper_name)] = str(nested_url)

                # save it to the pdf responses above for podcast generation
                self.pdf_responses.append(response)

    def check_if_paper_exists(self, paper_name):
        # get the list of directories within paperswithcode 
        outside_dir = '/'.join(self.download_location.split('/')[:-1])
        if [directory for directory in list(glob.glob(os.path.join(f"{outside_dir}", '*'))) if f"{paper_name}.pdf" in list(os.listdir(directory))]:
            return True
        else:
            return False