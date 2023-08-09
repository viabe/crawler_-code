import requests
headers={
    "User-agent": "Android",
    "Referer" : "http://www.nate.com"

}

response=requests.get("http://www.nate.com",
                      headers=headers,
)
fd = open("a.html","wb")
fd.write(response.content)
fd.close()
print(response.content)