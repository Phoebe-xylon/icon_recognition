import time
from urllib.parse import *
import requests
from utils.enc import aes_cbc_encrypt,str_to_md5
from utils.icon_recognition import recognition



def sign(payload):
    
    sign_list = [f"{k}={unquote(payload[k])}"  for k in ["appid","business_site","version","dimensions","extend_param"]]

    concatenated_string = "&".join(sign_list)
    result_hash =  str_to_md5(concatenated_string)
    return result_hash

url = "https://ic.ctrip.com/captcha/v4/risk_inspect"


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://flights.ctrip.com",
    "priority": "u=1, i",
    "referer": "https://flights.ctrip.com/",
    "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}



payload = {}

payload["extend_param"]=quote(aes_cbc_encrypt('{"resolution_width":1920,"resolution_height":1080,"language":""}'))
payload["appid"]= "100008370"
payload["business_site"]= "search_airticketscivil_online_pic"
payload["version"]= "2.0.30"


str = r'{"rt":undefined,"ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36","p":"pc","fp":null,"vid":"1754637465383.3291rvFwOPLC","sfp":undefined,"identify":null,"svid":undefined,"guid":null,"h5_duid":null,"pc_duid":null,"hb_uid":null,"pc_uid":null,"h5_uid":null,"infosec_openid":null,"device_id":null,"client_id":null,"pid":"1402104526868933","sid":"LTOOUojJFKDKhYLJ","login_uid":null,"client_type":"PC","site":{"type":"PC","url":"https://flights.ctrip.com/online/list/oneway-can-kwe?depdate=2025-09-29&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1","ref":"","title":"广州到贵阳机票查询预订-广州飞贵阳特价机票价格-携程飞机票","keywords":"广州到贵阳机票,广州到贵阳飞机票,广州到贵阳特价机票,携程飞机票"},"device":{"width":1920,"height":1080,"os":"","pixelRatio":1,"did":""},"user":{"tid":"","uid":"","vid":""}}'
payload["dimensions"]= quote(aes_cbc_encrypt(str))
payload["t"]= int(time.time()*1000)
signature = sign(payload=payload)
payload["sign"] =  signature
print(payload)
response = requests.post(url, json=payload, headers=headers)
risk_info = response.json()["result"]["risk_info"]
if risk_info["process_type"]=="ICON":
    small_image_b64 = risk_info["process_value"]["small_image"]  # 滑块图（模板来源）
    big_image_b64   = risk_info["process_value"]["big_image"]    # 背景图（搜索目标）
    print(recognition(big_image_b64,small_image_b64,True))
else:
    raise ValueError(f"not found process_type: {risk_info['process_type']}")

# print(response.json())