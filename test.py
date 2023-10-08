import requests
import json

# VIDEO_ID = '9707b93ea7fae3b9e65046c4d47f4b52'
# API_SECRET_KEY = ''

url = f"https://dev.vdocipher.com/api/videos/9707b93ea7fae3b9e65046c4d47f4b52/otp"

payloadStr = json.dumps({'ttl': 300})
headers = {
  'Authorization': "Apisecret duVqEvxX60rDRdbsrumTjRrBwk6KYyCMo4SJL9CR1D7iTSsbv6OxaNiXMSskXh3t",
  'Content-Type': "application/json",
  'Accept': "application/json"
}

response = requests.request("POST", url, data=payloadStr, headers=headers)

json_data = json.loads(response.text)

otp_value = json_data.get('otp')
playback_info_value = json_data.get('playbackInfo')

print("OTP:", otp_value)
print("Playback Info:", playback_info_value)
# print("HEllo word")