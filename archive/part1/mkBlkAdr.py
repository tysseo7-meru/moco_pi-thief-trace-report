

#import json
#import simplejson as json

'''
input: out file of piTracePayments.py

output:

ATH以上のPiを受けっとた送受信総額とアドレスリスト。ただし、送受信総額がATH(ex:999)ｘTIMES_SEND(ex:5回)未満はリストアップしない。

'''


import re
import sys

args = sys.argv

#print(args[0])
#print(args[1])

key_line="created_at"
id_am=1
id_fr=3
id_to=5

ATH=999
TIMES_SEND=5

s_in = args[1]

f = open(s_in, 'r')
data = f.read()
f.close()

ll=data.split()

#print(ll[0])
#lll=ll[0].split(",")
#print(lll[1])

l1=[]

pat='.*'+key_line+'.*'
for xxx in ll:
  if re.match(pat,xxx):
    l1.append(xxx)

d_adr_to={}
for xxx in l1:
  l2=xxx.split(",")
  f_am=float(l2[id_am])
  s_fr=l2[id_fr]
  s_to=l2[id_to]

  if f_am > ATH :
    if s_to not in d_adr_to:
      d_adr_to[s_to]=f_am
    else:
      d_adr_to[s_to]+=f_am

#print(d_adr_to)


l_adr_to_s = sorted(d_adr_to.items(), key=lambda x:x[1], reverse=True)

#print(l_adr_to_s)
ii=0
l_black_adr=[]
for tpl in l_adr_to_s:
  adr    = tpl[0]
  amound = tpl[1]
  if  amound >= ATH * TIMES_SEND:
    ii+=1
    print(ii,adr,amound)
    l_black_adr.append(adr)

print ("num of l_adr_to_s",len(l_adr_to_s))


