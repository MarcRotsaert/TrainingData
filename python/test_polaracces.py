# POLAR API TESTING

import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic dGhpc2RvZXNudDpkb2FueXRoaW6s",
    "Accept": "application/json",
}
body = {
    "grant_type": "authorization_code",
    "authorization_code": "SplxlOBeZQQYbYS6WxSbIA",
}

r = requests.post("https://polarremote.com/v2/oauth2/token", data=body, headers=headers)

print(r.json())
