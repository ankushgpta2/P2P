import yaml
from yaml.loader import SafeLoader
from datetime import datetime
from datetime import date
from twilio.rest import Client

"""
Uses Twilio account to automate the text messaging procedure to your phone 
It is based on the personal information stored within the text_info.yaml file 
"""

def send_text(paper_information, path_2_text_yaml):

    # get the datetime for text message
    now = datetime.now()
    date_n_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # construct the text message with the paper links and paper names
    text_to_send = f"\nHello From WebScraper Bot for paperswithcode.com! 🤖 \n\n" + \
                   f"Here is the list of papers that were downloaded for {date_n_time}: \n\n"
    for name,link in zip(paper_information.keys(), paper_information.values()):
        text_to_send += f"{name}: {link}\n\n"
    text_to_send += '\nThe script used to generate this message runs every 12 hours (Codebase: https://github.com/ankushgpta2).'

    # get the information from the text yaml specified 
    with open(path_2_text_yaml) as f:
        personal_info = yaml.load(f, Loader=SafeLoader)
        try:
            assert 'mobile_num' in personal_info.keys()
            assert 'num' in personal_info['twilio'].keys() and 'account_sid' in personal_info['twilio'].keys() \
                   and 'auth_token' in personal_info['twilio'].keys()
        except AssertionError:
            raise AssertionError(f"Missing information in .yaml file ({path_2_text_yaml})... please reference text_info_template.yaml on required information")

    # send the information out to twilio and then the text to mobile number 
    account_sid = str(personal_info['twilio']['account_sid'])
    auth_token = str(personal_info['twilio']['auth_token'])
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=text_to_send, to=str(personal_info['mobile_num']), from_=str(personal_info['twilio']['num']))
    except:
        print('🚨 Error connecting to Twilio client')