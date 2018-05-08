import json

with open('data.json','r') as f:
    s=f.read()
    data = json.loads(s)

for x in data['features']:
    ori_name = x['properties']['SSC_NAME']
    x['properties']['SSC_NAME'] = ori_name.split("(")[0].rstrip()

with open('education&incoming.json','w') as fw:
    json.dump(data,fw)
