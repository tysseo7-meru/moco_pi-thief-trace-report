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
i_api=0


def date2unixtime ( date ):
  date = date.replace('Z','')
  date = date.replace('T', ' ')
  ot = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
  return(ot.timestamp())

def adr2dict( addr , cursor , limit ):
  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/accounts/" + addr + "/payments?cursor=" +  str(cursor) + "&limit=" + str(limit) +"&order=asc"
  session = requests.Session()
  dd = session.get(url, timeout=301)
  jd = json.loads(dd.text)
  return jd



def listPayments( d_json , l_adr_may_not_checked):
  l_pays=[]
  id="unkown"
  errmsg="d_json in listPayments is NOT expected"
  if not ( '_embedded' in d_json.keys() ):
    print( errmsg )
  else:
    if not ( 'records' in d_json['_embedded'].keys() ):
      print( errmsg )
    else:
      l_adr = d_json['_embedded']['records']
      for dd in l_adr:
        #l_pays.append(dd)
        errmsg="Dict 'dd' in listPayments is unexpected data. "
        if not ( 'type' in dd.keys()):
          print(errmsg)
        else:
          if (dd['type']=="payment"):
            amount = dd['amount']
            if ( float(amount) > AMTH -1 ):
              buf = ""


              buf = buf + 'amount'
              buf = buf + ','
              buf = buf + dd['amount']
              buf = buf + ','
              buf = buf + 'from'
              buf = buf + ','
              buf = buf + dd['from']
              buf = buf + ','
              buf = buf + 'to'
              buf = buf + ','
              buf = buf + dd['to']
              buf = buf + ','
              buf = buf + 'created_at'
              buf = buf + ','
              buf = buf + dd['created_at']
              buf = buf + ','
              buf = buf + 'ut'
              buf = buf + ','
              ut = int(date2unixtime(dd['created_at']))
              buf = buf + str(ut)
              buf = buf + ','
              #print(buf)
              l_log.append(buf)
              l_pays.append(buf)


#d_adr_send={}
#d_adr_recv={}
              #####

              if f_mode != 1:
                if not ( dd['from'] in d_adr_send.keys()):
                  d_adr_send[dd['from']]=float(dd['amount'])
                  l_adr_may_not_checked.append(dd['from'])
                else:
                  d_adr_send[dd['from']]+=float(dd['amount'])
                  l_adr_may_not_checked.append(dd['from'])

              if f_mode != 2:
                if not ( dd['to'] in d_adr_recv.keys()):
                  d_adr_recv[dd['to']]=float(dd['amount'])
                  l_adr_may_not_checked.append(dd['to'])
                else:
                  d_adr_recv[dd['to']]+=float(dd['amount'])
                  l_adr_may_not_checked.append(dd['to'])

      #print("##l_adr_may_not_checked",len(l_adr_may_not_checked))
      #print(list(set(l_adr_may_not_checked)))







      #id =  l_adr[ -1 ]['id']
      id =  l_adr[ -1 ]['paging_token']
  return id, l_pays




def roopListPayments ( d_json , adress, l_adr_may_not_checked ):
  global i_api
  l_pays_tmp=[]
  l_pays=[]
  while True:
    errmsg="d_json in listPayments is NOT expected"
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
          next_cs , l_pays_tmp = listPayments(d_json,l_adr_may_not_checked)
          l_pays.extend(l_pays_tmp)
          d_json=adr2dict( adress , next_cs , LIM)
          i_api+=1
          #print("### DEBUG :",i_api)
  return(l_pays)





def pList1st ( root_adr ,l_adr_may_not_checked):
  global i_api
  l_pays=[]
  if  root_adr not in l_adr_checked:
    djson=adr2dict( root_adr , "" , LIM)
    l_pays=roopListPayments( djson , root_adr,l_adr_may_not_checked )
  l_adr_checked.append(root_adr)
  return l_pays

def pList ( root_adr ,l_adr_may_not_checked):
  global i_api
  l_pays_tmp=[]
  l_pays=[]
  d_pays={}

 
  l_adr_may_not_checked=[]
  l_pays_tmp=pList1st ( root_adr ,l_adr_may_not_checked)
  l_pays.append(l_pays_tmp)
  d_pays[root_adr]=l_pays

  for a in l_adr_may_not_checked:
    if not a in l_adr_checked:
      l_adr_not_checked.append(a)
  while(len(l_adr_not_checked)!=0):
    for aa in l_adr_not_checked:
      l_adr_may_not_checked=[]
      l_pays_tmp=pList1st(aa, l_adr_may_not_checked)
      l_pays.append(l_pays_tmp)
      d_pays[aa]=l_pays
 

      for a in l_adr_may_not_checked:
        if not a in l_adr_checked:
          l_adr_not_checked.append(a)
      l_adr_not_checked.remove(aa)


  '''
  for key in d_pays:
    #print(key, d_pays[key], sep=',')
    print("### "+key+" ###")
    for lll in d_pays[key]:
      for ll in lll:
        print(type(ll))
  '''
  return d_pays


def monSum():
  ### monitor d_adr_send, d_adr_recv ####

  print("#### from adress ####")
  d_adr_send_s = sorted(d_adr_send.items(),key=lambda x:x[1], reverse=True)
  i=0
  for key, value in d_adr_send_s:
    i+=1
    print(i, key, value, sep=',')

  print("#### to adress ####")
  d_adr_recv_s=sorted(d_adr_recv.items(),key=lambda x:x[1], reverse=True)
  i=0
  for key, value in d_adr_recv_s:
    i+=1
    print(i, key, value, sep=',')




  print("#### balances ####")
  l_merge_addr=[]
  for k in d_adr_send:
    l_merge_addr.append(k)
  for k in d_adr_recv:
    l_merge_addr.append(k)

  l_merge_addr = list(set(l_merge_addr))

  #print(l_merge_addr)
  #exit()
##################################
  d_mrg_bl={}
  i=0
  for k in l_merge_addr:
    i+=1
    url="https://api.mainnet.minepi.com/accounts/" + k 
    session = requests.Session()
    dd = session.get(url, timeout=10)
    jd = json.loads(dd.text)
    balance = jd['balances'][0]['balance']
    d_mrg_bl[k]=float(balance)
    #print(type(d_mrg_bl[k]))

  d_mrg_bl_s=sorted(d_mrg_bl.items(),key=lambda x:x[1], reverse=True)
  i=0
  for key, value in d_mrg_bl_s:
    i+=1
    print(i, key, value, sep=',')




