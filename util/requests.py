import urllib2
import json

'''
POST request example using python 2.7 
can be done using curl
curl -v -H "X-ApiKey: xxx" -H "Content-Type: application/json" --data '{"k1":"v1", "k2":"v2"}'  http://localhost:5000/api/rest/1/...

'''
url = 'http://localhost:5000/api/rest' 
post_fields = {'key': 'value'}  

data = json.dumps(post_fields)
request = urllib2.Request(url, data)
request.add_header('X-ApiKey', 'xxx')
request.add_header('Content-Type', 'application/json')
request.add_header('Content-Length', len(data))

response = urllib2.urlopen(request)
data = response.read()
print data
