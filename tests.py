import requests
import json

url = 'http://127.0.0.1:8080'

print('GET Method:')

print('\nTime in server zone -\t' + requests.get(url).text)

print('\nTime in time zone -\t' + requests.get(url+'/Asia/Almaty').text)


print('\nPOST Method:')

data = {'tz_start': 'Africa/Blantyre', 'type': 'date'}
print('\nDate -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Africa/Blantyre', 'type': 'time'}
print('\nTime -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Africa/Blantyre', 'tz_end': 'Europe/Moscow', 'type': 'datedif'}
print('\nDifference -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Australia/Melbourne', 'tz_end': 'Poland', 'type': 'datedif'}
print('\nDifference -\t' + requests.post(url=url, data=json.dumps(data)).text)
