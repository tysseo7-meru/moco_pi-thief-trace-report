
#### pip install requests

import json
import requests
import sys
import re
import datetime

LIM=200
AMTH=0
d_adr_send={}
d_adr_recv={}
l_adr_checked=[]

num_spam=0
num_trade=0
prev_ut=0

args = sys.argv
#root_adr    = str(args[1])

#print("==============================")
#print(type(args))

f_mode = 0

for xxx in args:
  if xxx=="-to":
    f_mode = 1
  if xxx=="-from":
    f_mode = 2






def adr2dict( addr , cursor , limit ):
  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/accounts/" + addr + "/payments?cursor=" +  str(cursor) + "&limit=" + str(limit) +"&order=asc"

  #print(url)
  session = requests.Session()
  dd = session.get(url)
  jd = json.loads(dd.text)
  return jd



def listPayments( d_json ,adr ):
  global num_spam
  global num_trade
  global prev_ut
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
              buf = buf + 'form'
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
              buf = buf + 'created_at(ut)'
              buf = buf + ','
              ut = int(date2unixtime(dd['created_at']))
              buf = buf + str(ut)
              buf = buf + ','
              buf = buf + 'delta(ut)'
              buf = buf + ','
              ut = int(date2unixtime(dd['created_at']))
              buf = buf + str(ut-prev_ut)
              buf = buf + ','
              print(buf)
              if ut-prev_ut < 60 and adr==dd['to']:
                num_spam+=1
              prev_ut=ut
              num_trade+=1





      id =  l_adr[ -1 ]['id']
  return id




def roopListPayments ( d_json , adress):
  global prev_ut
  global num_spam
  global num_trade
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
          next_cs = listPayments(d_json ,adress)
          d_json=adr2dict( adress , next_cs , LIM)



def pList ( adr ):
  if  adr not in l_adr_checked:
    djson=adr2dict( adr , "" , LIM)
    roopListPayments( djson , adr )

def pList2 ( adr ):
    global prev_ut
    global num_spam
    global num_trade
    
    prev_ut=0
    num_spam = 0
    num_trade = 0
    djson=adr2dict( adr , "" , LIM)
    roopListPayments( djson , adr  )


#UTC -> unixtime
def date2unixtime ( date ):
  date = date.replace('Z','')
  date = date.replace('T', ' ')
  ot = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
  return(ot.timestamp())


####################


'''
#test
l_adr=[
  "GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF",
  "GBFF6AGW2TBXKBEGJAKMXPYV3MRTGCIJ74J66YSBOILBMJRRGLSLJWV5",
  "GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU"
]
'''

#High spam_score adress
l_adr=[
  'GC3ZUA5QA6E4GWF5SMK2IWRDTWPFAO3QFXUWT3MH6PQAN3PUJW22UHSA',
]

#spam_score :The number of tranfer with in 60sec.

ii=0
l_spam_sore=[]
for adr in l_adr:
  ii+=1
  pList2(adr)
  l_spam_sore.append([ii,"spam_score:",num_spam,adr])

for ll in l_spam_sore:
  print(ll)
