#### python -m pip install --upgrade pip setuptools
#### pip install requests
#### pip install simplejson

#import json
import simplejson as json


import requests
import sys
import re
import datetime

f_mode = 0
LIM=200
AMTH=1000
d_adr_send={}
d_adr_recv={}
l_adr_checked=[]
l_adr_may_not_checked=[]
l_adr_not_checked=[]
l_log=[]


def date2unixtime ( date ):
  date = date.replace('Z','')
  date = date.replace('T', ' ')
  ot = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
  return(ot.timestamp())

def adr2dict( addr , cursor , limit ):
  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/accounts/" + addr + "/effects?cursor=" +  str(cursor) + "&limit=" + str(limit) +"&order=asc"
  session = requests.Session()
  dd = session.get(url)
  jd = json.loads(dd.text)
  return jd



def listEffects( d_json , predicate):
  id="unkown"
  predicate=[]
  errmsg="d_json in listEffects is NOT expected"
  if not ( '_embedded' in d_json.keys() ):
    print( errmsg )
  else:
    if not ( 'records' in d_json['_embedded'].keys() ):
      print( errmsg )
    else:
      l_adr = d_json['_embedded']['records']
      for dd in l_adr:
        errmsg="Dict 'dd' in listEffects is unexpected data. "
        if not ( 'type' in dd.keys()):
          print(errmsg)
        else:
          #if (dd['type']=="claimable_balance_claimant_created"):
          ii=0


          ##DEBUG##
          s_param='type'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')
          s_param='type_i'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')
          s_param='account'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')



          if ( 'predicate' in dd ):
              ii+=1
              #predicate = list(dd['predicate']).append(dd['created_at'])
              predicate.append(int(dd['predicate']['not']['rel_before']))
              predicate.append(dd['created_at'])
              #l_log.append(buf)
              #print(ii,predicate)

      id =  l_adr[ -1 ]['paging_token']
      #print("###id",id)
  return id, predicate




def roopListEffects ( d_json , adress, ll_dummy ):
  l_prd=[]
  l_prdtmp=[]
  while True:
    errmsg="d_json in listEffects is NOT expected"
    if not ( '_embedded' in d_json.keys() ):
      print( errmsg )
      break
    else:
      if not ( 'records' in d_json['_embedded'].keys() ):
        print( errmsg )
        break
      else:
        l_adr = d_json['_embedded']['records']
        if(len(l_adr)==0):
          break
        else:
          next_cs , l_prdtmp= listEffects(d_json,ll_dummy)
          if len(l_prdtmp) !=0:
             l_prd.extend(l_prdtmp)
             #print(predicate)
          d_json=adr2dict( adress , next_cs , LIM)
  return l_prd




def pList1st ( root_adr ,l_dummy):
  if  root_adr not in l_adr_checked:
    djson=adr2dict( root_adr , "" , LIM)
    predicate=roopListEffects( djson , root_adr,l_dummy )
  return predicate

l_adr=[
  'GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU',
  'GDISC3J222YP5DEOJ6FJQGCRLRA2R3FFZPCTREXGQNUXWGGPNJ5AQG27',
  'GARKPUF7VEI7EDNXIVUGIMSXN5TJKTAKH3J3LF2E7HTZQJWB6SKE4M4L',
  'GDIZUA3WX2AOOIR3VUE2NU357JJTZEAFR5P6VGK6KEWDP766ZV6CIRRB'

]




l_dummy=[]
predicate=[]

l_spam_sore=[]

ii=0
for adr in l_adr:
  predicate=[]
  predicate=pList1st(adr,l_dummy)
  ii+=1
  #print("#",adr,predicate,len(predicate))
  if(len(predicate)!=0):
    ii=0
    for xxx in predicate:
      if(ii%2==0):
        print(adr,predicate[ii+1],predicate[ii],sep=',')
      ii+=1






