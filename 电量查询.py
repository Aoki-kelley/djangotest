import requests
import re
import os
url=r'http://211.64.143.63/hyChage/kdroom/getRoomAmp?roomid=1166&xiaoquid=2'
r=requests.get(url)
r.encoding=r.apparent_encoding
with open(r'C:\Users\USER\Desktop\spider-test\5.txt','w+') as f:
    f.write(r.text)
xiaoqu=re.findall(':"[\s\S]*?"',re.findall('"xiaoqu":"[\s\S]*?"',r.text)[0])[0].replace(':','').replace('"','')
room=re.findall(':"[\s\S]*?"',re.findall('"room":"[\s\S]*?"},',r.text)[0])[0].replace(':','').replace('"','')
l=room.split('#')
reset_charge=re.findall(':[\s\S]*?,',re.findall('"restAmp":[\s\S]*?,',r.text)[0])[0].replace(':','').replace(',','')
print('校区:{0}\n楼区:{1}\n宿舍:{2}\n剩余电量:{3}'.format(xiaoqu,l[0],l[1],float(reset_charge)))
os.system("pause")
