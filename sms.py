import urllib

# Please see the FAQ regarding HTTPS (port 443) and HTTP (port 80/5567)
sms = "esto es una prueba de sms "

#url = "http://bulksms.2way.co.za/eapi/submission/send_sms/2/2.0"
url = 'https://bulksms.vsms.net/eapi/submission/send_sms/2/2.0'
      #'https://bulksms.vsms.net/eapi/submission/send_sms/2/2.0'
params = urllib.urlencode({'username' : 'manuelibarra', 'password' : 'irma3333', 'message' : sms , 'msisdn' : 51927615565})
f = urllib.urlopen(url, params)

s = f.read()

result = s.split('|')
statusCode = result[0]
statusString = result[1]
if statusCode != '0':
    print "Error: " + statusCode + ": " + statusString
else:
    print "Message sent: batch ID " + result[2]

