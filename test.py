# Python program to read
# json file


import json


f = open('data.json',)


data = json.load(f)

print(data[:10])


f.close()
