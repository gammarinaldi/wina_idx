import requests

def call(access_token, trade_id):
    try:
        url = f"https://ht2.ajaib.co.id/api/v1/stock/auto-trading/{trade_id}/cancel/"

        payload={}
        headers = {
        'authority': 'ht2.ajaib.co.id',
        'accept': '*/*',
        'accept-language': 'id',
        'authorization': access_token,
        'content-length': '0',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://invest.ajaib.co.id',
        'referer': 'https://invest.ajaib.co.id/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-ht-ver-id': '0322b9396fc0f476309aeafbbbe4e72d210e5c8f5815abf1fde7503b9126086e3e6d000a5f255765e8db3489c563a8fa950870c8920099ba073a08590d3da722',
        'x-platform': 'WEB',
        'x-product': 'stock-mf'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        return response
    except requests.exceptions.HTTPError as errh:
        return "Http Error: ", errh
    except requests.exceptions.ConnectionError as errc:
        return "Error Connecting: ", errc
    except requests.exceptions.Timeout as errt:
        return "Timeout Error: ", errt
    except requests.exceptions.RequestException as err:
        return "Oops.. Something Else: ", err
    
