import http.client
import urllib.parse
import json


def processGETRequest(appKey, token, text, audioSaveFile, format, sampleRate):
    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # set URL request parameters
    url = url + '?appkey=' + appKey
    url = url + '&token=' + token
    url = url + '&text=' + text
    url = url + '&format=' + format
    url = url + '&sample_rate=' + str(sampleRate)
    # voice，default xiaoyun。
    url = url + '&voice=' + 'ailun'
    # volume 音量，范围是0~100，可选，默认50。
    url = url + '&volume=' + str(50)
    # speech_rate 语速，范围是-500~500，可选，默认是0。
    url = url + '&speech_rate=' + str(0)
    # pitch_rate 语调，范围是-500~500，可选，默认是0。
    url = url + '&pitch_rate=' + str(0)
    print(url)
    conn = http.client.HTTPSConnection(host)
    conn.request(method='GET', url=url)
    # process response from server end
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    print(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType:
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        print('The GET request succeed!')
    else:
        print('The GET request failed: ' + str(body))
    conn.close()


def processPOSTRequest(appKey, token, text, audioSaveFile, format, sampleRate):
    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # set HTTPS Headers。
    httpHeaders = {
        'Content-Type': 'application/json'
    }
    # set HTTPS Body。
    body = {'appkey': appKey, 'token': token, 'text': text, 'format': format, 'sample_rate': sampleRate}
    body = json.dumps(body)
    print('The POST request body content: ' + body)

    conn = http.client.HTTPSConnection(host)
    conn.request(method='POST', url=url, body=body, headers=httpHeaders)
    # process response from server end
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    print(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType:
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        print('The POST request succeed!')
    else:
        print('The POST request failed: ' + str(body))
    conn.close()


from alibaba_oauth_token import get_alibaba_token

appKey = "1GAPpb2VqpBa69V6"
token = get_alibaba_token()
text = '大壮正想去摘取花瓣，谁知阿丽和阿强突然内讧，阿丽拿去手枪向树干边的阿强射击，两声枪响，阿强直接倒入水中'
# Use RFC 3986 for urlencode encoding.
textUrlencode = text

textUrlencode = urllib.parse.quote_plus(textUrlencode)
textUrlencode = textUrlencode.replace("+", "%20")
textUrlencode = textUrlencode.replace("*", "%2A")
textUrlencode = textUrlencode.replace("%7E", "~")
print('text: ' + textUrlencode)
audioSaveFile = 'output/syAudio.wav'
format = 'wav'
sampleRate = 16000
# use GET request
processGETRequest(appKey, token, textUrlencode, audioSaveFile, format, sampleRate)
# use POST request
# processPOSTRequest(appKey, token, text, audioSaveFile, format, sampleRate)
