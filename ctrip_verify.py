import time
import random
from urllib.parse import *
import requests
from utils.enc import aes_cbc_encrypt,str_to_md5
from utils.icon_recognition import recognition



def sign(payload,key = "init"):
    if key=="init":
        sign_list = [f"{k}={unquote(payload[k])}"  for k in ["appid","business_site","version","dimensions","extend_param"]]
    elif key=="verify":
        sign_list = [f"{k}={unquote(payload[k])}"  for k in ["appid","business_site","version","verify_msg","dimensions","extend_param","token"]]
        sign_list.append("captcha_type=ICON")

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


ua_str = r'{"rt":undefined,"ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36","p":"pc","fp":null,"vid":"1754637465383.3291rvFwOPLC","sfp":undefined,"identify":null,"svid":undefined,"guid":null,"h5_duid":null,"pc_duid":null,"hb_uid":null,"pc_uid":null,"h5_uid":null,"infosec_openid":null,"device_id":null,"client_id":null,"pid":"1402104526868933","sid":"LTOOUojJFKDKhYLJ","login_uid":null,"client_type":"PC","site":{"type":"PC","url":"https://flights.ctrip.com/online/list/oneway-can-kwe?depdate=2025-09-29&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1","ref":"","title":"广州到贵阳机票查询预订-广州飞贵阳特价机票价格-携程飞机票","keywords":"广州到贵阳机票,广州到贵阳飞机票,广州到贵阳特价机票,携程飞机票"},"device":{"width":1920,"height":1080,"os":"","pixelRatio":1,"did":""},"user":{"tid":"","uid":"","vid":""}}'
payload["dimensions"]= quote(aes_cbc_encrypt(ua_str))
payload["t"]= int(time.time()*1000)
signature = sign(payload=payload)
payload["sign"] =  signature
print(payload)
response = requests.post(url, json=payload, headers=headers)
token = response.json()["result"]["token"]
rid = response.json()["result"]["rid"]
risk_info = response.json()["result"]["risk_info"]
if risk_info["process_type"]=="ICON":
    small_image_b64 = risk_info["process_value"]["small_image"]  # 滑块图（模板来源）
    big_image_b64   = risk_info["process_value"]["big_image"]    # 背景图（搜索目标）
    result = recognition(big_image_b64,small_image_b64,False)
else:
    raise ValueError(f"not found process_type: {risk_info['process_type']}")

url = "https://ic.ctrip.com/captcha/v4/verify_icon"


payload = {}

payload["token"] = token
payload["rid"] = rid
payload["extend_param"]=quote(aes_cbc_encrypt('{"resolution_width":1920,"resolution_height":1080,"language":""}'))
payload["appid"]= "100008370"
payload["business_site"]= "search_airticketscivil_online_pic"
payload["version"]= "2.0.30"
durtime = random.randint(5500,6500)
st = int(time.time()*1000)-durtime
end = int(time.time()*1000)
iconViewDuration = durtime+random.randint(100,500)
durtime = str(durtime)
verify_msg = '{"st":undefined,"display":"1920x1080","keykoardTrack":[],"iconKeyboardEventExist":false,"iconViewDuration":'+str(iconViewDuration)+',"timezone":-480,"flashState":false,"language":"zh-CN","platform":"MacIntel","cpuClass":undefined,"hasSessStorage":true,"hasLocalStorage":true,"hasIndexedDB":true,"hasDataBase":false,"doNotTrack":false,"touchSupport":false,"mediaStreamTrack":true,"preIconClickTrack":[{"x":1025,"y":498,"t":'+str(st+3120)+'},{"x":1025,"y":498,"t":'+str(st+3120)+'},{"x":1026,"y":498,"t":'+str(st+3126)+'},{"x":1026,"y":498,"t":'+str(st+3133)+'},{"x":1027,"y":498,"t":'+str(st+3141)+'},{"x":1027,"y":498,"t":'+str(st+3148)+'},{"x":1028,"y":498,"t":'+str(st+3157)+'},{"x":1028,"y":498,"t":'+str(st+3165)+'},{"x":1028,"y":498,"t":'+str(st+3173)+'},{"x":1028,"y":498,"t":'+str(st+3180)+'},{"x":1029,"y":498,"t":'+str(st+3196)+'},{"x":1029,"y":499,"t":'+str(st+3254)+'},{"x":1029,"y":499,"t":'+str(st+3261)+'},{"x":1029,"y":499,"t":'+str(st+3285)+'},{"x":1029,"y":499,"t":'+str(st+3300)+'},{"x":1030,"y":499,"t":'+str(st+3308)+'},{"x":1030,"y":499,"t":'+str(st+3314)+'},{"x":1030,"y":499,"t":'+str(st+3322)+'},{"x":1031,"y":499,"t":'+str(st+3330)+'},{"x":1031,"y":499,"t":'+str(st+3338)+'},{"x":1031,"y":499,"t":'+str(st+3362)+'}],"iconClickTrack":"","inputStartTs":'+str(st)+',"inputEndTs":'+str(end)+',"inputTime":'+str(durtime)+',"selectMoveTrace":"","selectMoveTime":"","selectCancelCount":0,"selectIsTruncation":true,"value":'+str(result)+'}'
payload["verify_msg"] = quote(aes_cbc_encrypt(verify_msg))
ua_str = r'{"rt":undefined,"ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36","p":"pc","fp":null,"vid":"1754637465383.3291rvFwOPLC","sfp":undefined,"identify":null,"svid":undefined,"guid":null,"h5_duid":null,"pc_duid":null,"hb_uid":null,"pc_uid":null,"h5_uid":null,"infosec_openid":null,"device_id":null,"client_id":null,"pid":"1402104526868933","sid":"LTOOUojJFKDKhYLJ","login_uid":null,"client_type":"PC","site":{"type":"PC","url":"https://flights.ctrip.com/online/list/oneway-can-kwe?depdate=2025-09-29&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1","ref":"","title":"广州到贵阳机票查询预订-广州飞贵阳特价机票价格-携程飞机票","keywords":"广州到贵阳机票,广州到贵阳飞机票,广州到贵阳特价机票,携程飞机票"},"device":{"width":1920,"height":1080,"os":"","pixelRatio":1,"did":""},"user":{"tid":"","uid":"","vid":""}}'
payload["dimensions"]= quote(aes_cbc_encrypt(ua_str))
payload["t"]= int(time.time()*1000)



signature = sign(payload=payload,key="verify")
payload["sign"] =  signature
response = requests.post(url, json=payload, headers=headers)
pass_verify = response.json()["result"]["risk_info"]["risk_level"]==0
print("risk_level:"+str(response.json()["result"]["risk_info"]["risk_level"]))
print("token:"+response.json()["result"]["token"]+",rid:"+response.json()["result"]["rid"])
token = response.json()["result"]["token"]
rid = response.json()["result"]["rid"]

url = "https://flights.ctrip.com/international/search/api/authcode/verifyPicAuthCode"

querystring = {"v":"0.022658366710042732"}

payload = {
    "version": "2.0.30",
    "token": token,
    "rid": rid
}
headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "cookie": 'cticket=4B859A0467115B18FC885CBC4E93DE82CC8AB049E5C0B1286F964AA0AF127EB0',
    "origin": "https://flights.ctrip.com",
    "priority": "u=1, i",
    "referer": "https://flights.ctrip.com/online/list/oneway-can-kwe?depdate=2025-10-03&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1",
    # "rms-token": "fp=68E79A-878C56-0B0AA7&vid=1754637465383.3291rvFwOPLC&pageId=10320673302&r=d8fff466ca704384b64a4c662779a522&ip=117.107.131.194&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F140.0.0.0%20Safari%2F537.36&d=flights.ctrip.com&v=25&kpg=0_0_0_0_0_0_0_0_0_0&adblock=F&cck=F&ftoken=",
    "scope": "d",
    "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sessionid": "14",
    "token": "1001-common-U5trDQjoOEqTjGBi48e98w6QwzGwcgisGy4LJksw4QwOdYahy9gwNLRhqjQtwhaRpcyHdJ13vBoWUqJhdjcQRdGj1hwg0jfbwFQYUtRPbvsBy7cJpBj1Y3gK4Ue63w1DRTMylBJBZvqtRphRB5Eg3YsZjbPYlmwZcjUQwlGEmGxtFRAY3geU3yaTEkqe9QwqUYGYfUj7yMlYTNRs9yhsJPojdgjqFwkcimkEX7JQljHmiBOimUYf0ItGYLfiGzvZajSqeNnv9NjFbRszJqsif8eQaEnsyNvQ8J7Y7fRnOJTdKdPvbHy7qWzBJhQEl6istyfUEoqe6HYSqYkaw1PvFoeAkEm6EfUvObwfteOTvAZJTZyoAJgqephEDhy7MYkcYLgv7fEoSJmqjfFvTpikOwn3wF6jL8r17vOY90xm7vSXxNoWtqjhkYF8wDSwSHRNsYqMwMQe4mIUDwPYs4Y8vtPIzUilFWFXySLJfzymYcpxP8E11K3BrTOEt3wzbxldYNtjTcjpdW88x9PjHUrtYQSYZhvtPWOLetZEScjZlWqLyHLv68Y1Yk9xGcjtXygkrF6KZaeoAEzkW8SxQNwmTYHYZSRhUi7DeNtRbgvN9YcnWpdedPRkHWacjgqWtPK09rloWtYPBKT0ezkJf0R0fvHXY9hW6BeSBRHBWaDJnmJ0gJDHi1G",
    "transactionid": "f4dcc06e2cf1461e81846e6d7b56ea9a",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
if pass_verify:
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    print(response.json())

# p08d0ba2773331f16e9d876624ea397a578e2d34c5463!REGION!SHA
# 5EBF46DAB28A4005A038DD54E6D6F3D1