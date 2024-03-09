import httpx
import time
import secrets
import string
import uuid
import jwt

key = "" #jwt secret key
Authorization = "" #Bearer access token
text = "hello!" 
file = "video.mp4"

def jwt_token(timestamp: str) -> str:
    payload = {
    "iat": int(timestamp),
    "exp": int(timestamp) + 5
    }
    jwt.api_jws.PyJWS.header_typ = False
    jwt_token = str(jwt.encode(payload=payload,key=key,algorithm="HS256"))
    return jwt_token

def main():
    times = time.time()
    timestamp = str(int(times))
    timestamp2 = str(int(times*1000))
    random_str = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    uuid_ = str(secrets.token_hex(8))
    headers = {
        'Host': 'api.yay.space',
        'User-Agent': 'yay 3.33.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'Authorization': Authorization,
        'X-Timestamp': timestamp,
        'X-App-Version': '3.33',
        'X-Device-Info': 'yay 3.33.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'X-Device-Uuid': uuid_,
        'X-Connection-Type': 'wifi',
        'X-Connection-Speed': '0 kbps',
        'Accept-Language': 'ja',
        # 'Accept-Encoding': 'gzip, deflate, br',
    }
    filepath = f'{random_str}_{timestamp2}.mp4'
    params = {'video_file_name': filepath}
    response = httpx.get('https://api.yay.space/v1/users/presigned_url', params=params, headers=headers, verify=False)
    print(response.json())
    presigned_url = str(response.json()["presigned_url"])

    headers = {
        'Host': 'yay-vod-input.s3.ap-northeast-1.amazonaws.com',
        'Content-Type': 'video/mp4',
        # 'Content-Length': '580132',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'okhttp/4.11.0',
        'Connection': 'close',
    }
    with open(file,"br") as f:
        data = f.read()
    response = httpx.put(presigned_url,headers=headers,data=data,verify=False,timeout=180)
    print(response)

    timestamp = str(int(time.time()))
    token = jwt_token(timestamp)
    headers = {
        'Host': 'api.yay.space',
        'X-Jwt': token,
        'User-Agent': 'yay 3.33.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'Authorization': Authorization,
        'X-Timestamp': timestamp,
        'X-App-Version': '3.33',
        'X-Device-Info': 'yay 3.33.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'X-Device-Uuid': uuid_,
        'X-Connection-Type': 'wifi',
        'X-Connection-Speed': '0 kbps',
        'Accept-Language': 'ja',
        'Content-Type': f'multipart/form-data; boundary={str(uuid.uuid4())}',
        # 'Content-Length': '1029',
        # 'Accept-Encoding': 'gzip, deflate, br',
    }
    files = {
        'text': (None, text.encode(), 'text/plain; charset=UTF-8', {'Content-Transfer-Encoding': 'binary', 'Content-Length': str(len(text))}),
        'font_size': (None, '0', 'text/plain; charset=UTF-8', {'Content-Transfer-Encoding': 'binary', 'Content-Length': '1'}),
        'color': (None, '0', 'text/plain; charset=UTF-8', {'Content-Transfer-Encoding': 'binary', 'Content-Length': '1'}),
        'post_type': (None, 'video', 'text/plain; charset=UTF-8', {'Content-Transfer-Encoding': 'binary', 'Content-Length': '5'}),
        'video_file_name': (None, filepath, 'text/plain; charset=UTF-8', {'Content-Transfer-Encoding': 'binary', 'Content-Length': str(len(filepath))}),
    }
    response = httpx.post('https://api.yay.space/v3/posts/new', headers=headers, files=files, verify=False)
    print(response.json())

if __name__ == "__main__":
    main()
