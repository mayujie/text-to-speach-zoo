import requests
import json


def main():
    # @TODO: Add here your API key and Secret Key
    API_KEY = ""
    SECRET_KEY = ""
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_KEY}&client_secret={SECRET_KEY}&grant_type=client_credentials"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    

if __name__ == '__main__':
    main()
