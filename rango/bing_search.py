########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'cab2b2732014469196c61d9b24ba8e5e',
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': 'bill gates',
    'count': '10',
    'offset': '0',
    'mkt': 'en-us',
    'safesearch': 'Moderate',
})

try:
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("GET", "/bing/v7.0/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################