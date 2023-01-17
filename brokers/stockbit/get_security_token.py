import requests

def call(access_token, proxies):
    try:
        url = "https://exodus.stockbit.com/sekuritas/auth/token"

        payload={}
        headers = {
            'authority': 'exodus.stockbit.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'authorization': access_token,
            'dnt': '1',
            'origin': 'https://stockbit.com',
            'referer': 'https://stockbit.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)

        return response
    except requests.exceptions.HTTPError as errh:
        return "Http Error: ", errh
    except requests.exceptions.ConnectionError as errc:
        return "Error Connecting: ", errc
    except requests.exceptions.Timeout as errt:
        return "Timeout Error: ", errt
    except requests.exceptions.RequestException as err:
        return "Oops.. Something Else: ", err
    
