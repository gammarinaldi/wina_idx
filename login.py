import requests
import json

def call(user):
    try:
        url = "https://ht2.ajaib.co.id/api/v6/login/"

        payload = json.dumps({
            "email": user["email"],
            "password": user["password"],
            "platform": "web"
        })

        headers = {
            'authority': 'ht2.ajaib.co.id',
            'accept': '*/*',
            'accept-language': 'id',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://login.ajaib.co.id',
            'referer': 'https://login.ajaib.co.id/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'x-ht-ver-id': '0322b9396fc0f476309aeafbbbe4e72d210e5c8f5815abf1fde7503b9126086e3e6d000a5f255765e8db3489c563a8fa950870c8920099ba073a08590d3da722'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response
    except requests.exceptions.HTTPError as errh:
        return "Http Error: ", errh
    except requests.exceptions.ConnectionError as errc:
        return "Error Connecting: ", errc
    except requests.exceptions.Timeout as errt:
        return "Timeout Error: ", errt
    except requests.exceptions.RequestException as err:
        return "Oops.. Something Else: ", err
