#### python -m pip install --upgrade pip setuptools
#### pip install requests
#### pip install simplejson
#### pip install numpy
#### pip install matplotlib


'''
(1) prLockInfo:
　Input: address list
　Output: address, migration date, lock period

(2) Modify piTracePayments_lib and change to piTracePayments_lib2 to return all blockchain data up to the top while leaving the result of piTracePayments as it is

(3) prStolenAdrsInfo
Input: thief address
Output: list of victim addresses, migration time, lock duration, stolen time

Victim address criteria
・The number of transmissions and receptions is 20 or less
・No mass remittance (AMTH default 1000)
・No deposit
・Balance less than 2π




'''

#import json
import simplejson as json
import os
import re
#import piTracePayments_lib2 as pt
import piTracePayments_lib3 as pt


import requests
import sys
import re
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import shutil



f_mode = 0
LIM=200
AMTH=1000
d_adr_send={}
d_adr_recv={}
l_adr_checked=[]
l_adr_may_not_checked=[]
l_adr_not_checked=[]
l_log=[]

DEF_STOLEN_BALANCE=2
#DEF_STOLEN_BALANCE=10

#requests.get('https://api.mainnet.minepi.com/accounts/', timeout=10)


def ut2date ( ut ):
  # Convert to unix time date
  return datetime.datetime.fromtimestamp(ut)


def date2unixtime ( date ):
  # Convert payment date to unix time


  date = date.replace('Z','')
  date = date.replace('T', ' ')
  date = date.replace('/', '-')
  ot = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
  return(ot.timestamp())

def adr2dictE( addr , cursor , limit ):
  '''
  Convert json of effect tab of specified address to dict. 
  The initial value of cursor is "". 
  After the second time, the last paging_token value displayed last time
  '''

  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/accounts/" + addr + "/effects?type=claimable_balance_claimant_created?cursor=" +  str(cursor) + "&limit=" + str(limit) +"&order=asc"
  session = requests.Session()
  #dd = session.get(url, timeout=10)
  dd = session_get(url,session)
  jd = json.loads(dd.text)
  return jd

def session_get(url,ses):
  return ses.get(url, timeout=305)

def l2dict( ledger , cursor ):

  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/ledgers/" + str(ledger) + "/operations??cursor=" +  str(cursor) + "&limit=200"
  session = requests.Session()
  #dd = session.get(url, timeout=10)
  dd = session_get(url,session)
  jd = json.loads(dd.text)
  return jd


def l2dict2( ledger ):

  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/ledgers/" + str(ledger)
  session = requests.Session()
  #dd = session.get(url, timeout=10)
  dd = session_get(url,session)
  jd = json.loads(dd.text)
  return jd


def listEffects( d_json , predicate):
  # Extract predicate as lock period from effect information (dict)

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
          '''
          s_param='type'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')
          s_param='type_i'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')
          s_param='account'
          if ( s_param in dd ):
            print("##",s_param,dd[s_param],sep=',')
          '''


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


#def getstolen_name(l_shief_adr):
#def getstolen_name(shief_adr):
def getstolen_name(shief_adr,f):

    print("### running getstolen_name ... ",shief_adr)


    l_stolen=prStolenAdrsInfo (shief_adr)
    #print(l_stolen)

    if len(l_stolen)<=1 :
      return 0
    print(  "shief_adr,"+shief_adr+str(",")+str(len(l_stolen)-1))
    f.write("shief_adr,"+shief_adr+str(",")+str(len(l_stolen)-1))
    f.write("\n")

    ii=0
    for xxx in l_stolen:
      #print(ii,xxx, sep=',')
      buf = "stolen by "
      buf += shief_adr[0]
      buf += shief_adr[1]
      buf += shief_adr[2]
      buf += shief_adr[3]
      buf += ","+ str(ii) + ","
      for xx in xxx:
        buf += str(xx) + ","
      print(buf)
      f.write(buf+'\n')
      ii+=1
    print("")
    f.write('\n\n')



def Run_getstolen_name( Nled , odir, ut_stop):
  #odir="out"
  if not os.path.isdir(odir):
    os.mkdir(odir)
  files = os.listdir(odir)
  for s in files:
    s = re.sub('\.txt$', '', s)
    l_ck.append(s)

  last_time=0
  flag_sleep=0
  n_ck_th = 98
  while True:
    jd=l2dict( Nled , "")
    #Nled+=1
    pt.i_api+=1
    ###Sleep
    last_time=SleepForAPI(Nled,last_time,flag_sleep)
    if '_embedded' in jd:
      for xx in jd['_embedded']['records']:
        #print(ut_stop, xx['created_at'], date2unixtime(xx['created_at']) )
        if date2unixtime(xx['created_at']) >= ut_stop:
          print("Exited by -stop option")
          exit()

        type=xx['type']
        if type == 'payment':
          amo = float(xx['amount'])
          frm = xx['from']
          if frm in l_ck:
            print(Nled,amo,frm,"(already checked)","  Napi:",pt.i_api)
          else:
            if amo<=n_ck_th:
              print(Nled,amo,frm,"(less than",n_ck_th,")","  Napi:",pt.i_api)
            else:
              print(Nled,amo,frm)
          if amo>n_ck_th and (frm not in l_ck):
            #print("#####getstolen_name####",frm)
            ofile = odir + '/' + frm + '.txt'
            f = open(ofile, 'w')
            dt_now = datetime.datetime.now()
            ut_s=int(date2unixtime(str(dt_now.strftime('%Y-%m-%d %H:%M:%S'))))
            f.write("Strat,"+str(dt_now))
            f.write("\n")
            getstolen_name(frm,f)

            print("### Napi",pt.i_api,"\n",sep=",")

            l_ck.append(frm)
            dt_now = datetime.datetime.now()
            ut_e=int(date2unixtime(str(dt_now.strftime('%Y-%m-%d %H:%M:%S'))))
            f.write("\nEnd,"+str(dt_now))
            f.write("\nRunTime,"+str(ut_e-ut_s)+",sec")
            f.write("\n")
            f.close()
            ###Sleep
            #last_time=SleepForAPI(Nled,last_time,flag_sleep)
      Nled+=1



    else:
      print("sleeping 5 sec....")
      time.sleep(5)


######################
def Run_getsMigBlance( Nled , ofile, ut_stop):
  '''
  l_ca=[['GCCBC6U2PAHQGY5QFYXPSX57DHFQKDK7S6Q2QN5RDVA3JCJWFNX5V5JQ', 9.636378, '2024-03-06T22:02:21Z'], ['GDRQAOKEZUO7GYLMM7LNV5Z66IB6XKKLGFIQSWMKYSFWGEEADVRF4GJB', 9.8496621, '2024-03-06T22:02:21Z'], ['GB7W3BSENZJMB4X6BEQF3J5ALHTJXIGGUHBBK26KQWLUVQPTQIMFTKSQ', 11.285272800000001, '2024-03-06T22:02:21Z'], ['GDTGBBX5OJYYIUHLBS5ZVKHGY6GJNIE53FOEFD43ICUMSKIEDG7MEZBQ', 24.035195299999998, '2024-03-06T22:02:21Z'], ['GDYKUR5XOHTSO7T4MRCYRALOGFE3XYDZPALZZK7X7WNHIM2P4TUMUUP3', 30.740359400000003, '2024-03-06T22:02:21Z'], ['GAN7CW43MTW6XXR46MNU657Q63DVK7OWNFXPMPTFFTDK3PGY6WF5FJL6', 36.1562864, '2024-03-06T22:02:21Z'], ['GBX3O67XQ2HLDKNKCAACKDE7Y7YNIQ3BLWSK7AAGHUJL5EGRUQOUFR2J', 43.8545944, '2024-03-06T22:02:21Z'], ['GA77A4Y7KNO5EJ747HVV4FFKHZ23YNXUUHT7R5YLJSCUAO5SY6SN4DAF', 44.173153, '2024-03-06T22:02:21Z'], ['GAE4WFII7HJFPMUGYM7J4ZETUOSD6WDC3KD5MAXWCHHAPT2D5QICR5ZT', 62.4360158, '2024-03-06T22:02:21Z'], ['GDTWAG7ROQ4EWBPL3OHC2GCIXGCK4SFVDGWNPSLT2P7EZLR5HSQNVMSS', 92.3996129, '2024-03-06T22:02:21Z'], ['GD4LLD6J75WZN7QK2BZYUHEXUZKGTWSXPSSFJD4ZXIYCK3TKGV4KMOYE', 131.5180854, '2024-03-06T22:02:21Z'], ['GAQO5R6EUWX56E5TK4UM442XXAZOCI7HIO4OWPOTJM7RFMITVRWFPY7C', 155.927935, '2024-03-06T22:02:21Z'], ['GAPAFJWJYGD4V4LXR7IZT6NS3OF6G7KNEMBMH6FGJN2KB4YUOILBFMCL', 163.3863245, '2024-03-06T22:02:21Z'], ['GASDB2OCA6XUQYK3HQL5FJ3GQMHYWFMHV3Y2W6K2PHTXVGZCVMIQL2QW', 249.0977862, '2024-03-06T22:02:21Z'], ['GA65TQ7ZMVP5UKRJYXYN36VE4GKWYFHV4QBTGGNZFF6B7ODP6FQHPEPD', 250.02561079999998, '2024-03-06T22:02:21Z'], ['GANWG32QU2XG2SGGZZWVXFPCOB4RJ6BA2E6CX6B4E7BB4QJY2RRPUEMU', 265.0981713, '2024-03-06T22:02:21Z'], ['GAG5NLPP5UOGNZOQIZITKADAKY6ZZSV75MTCK355WLE7MBFMI67XJCF2', 321.9532791, '2024-03-06T22:02:21Z'], ['GA5BSVAS25UYRHH7PPP2F7H3XXYM7A2G3O4HBKKEUHQMBYZWNJGFNQ3A', 330.8225467, '2024-03-06T22:02:21Z'], ['GBHSIR2QOKSAWI5HF7RLFUCI7YAVXW23R6A6Y6IIQNAU3WXFSL7TSPRI', 382.2387657, '2024-03-06T22:02:21Z'], ['GBMNBEXMSSVFXCR5N5M5NLYANTF55VWTJCYWBXB4NXXUCBQ76GEHJEHY', 393.3892537, '2024-03-06T22:02:21Z'], ['GAP22FRNZGNXVQZFK6KQ4236YXCL3BU4JGDSU3GQZJRQ4IH7Q6RPKISU', 396.2271704, '2024-03-06T22:02:21Z'], ['GA2MOLJWEGLFRZGD5G2UICXVXUSGMCBMI6A6V3DTGQ3QMGYR6Q36TXAM', 460.7707375, '2024-03-06T22:02:21Z'], ['GCTZKUKYTCGUSIDZXU6BDMZTOJGZLCL3O2CBJXQNAERUVURJXP72IHIF', 643.3414169, '2024-03-06T22:02:21Z'], ['GCI63DMKTX55IJNV2U7FLKNMVGNFQVVP5SGGC3SEFRLQBMTXVUEKTOY2', 645.6069658, '2024-03-06T22:02:21Z'], ['GCW7XFHEWEZMQ2Z7TKPBGU37Y5ODWZEG5TMCCGYDW7XT2EEBLCCWRP3E', 944.8878227, '2024-03-06T22:02:21Z'], ['GDAHL4ZW7Y63PTSIN37KWNYQBQDJQSDDVA735IDDYB4HXP4JMQNPN6T2', 1258.8817464, '2024-03-06T22:02:21Z'], ['GAKEUJUE5XWENR4MW2PCISBG5HP76MOKRT5THLZQ3EM7TI46FT67CU22', 1349.9740377, '2024-03-06T22:02:21Z'], ['GBRREVKQHQTZBLUZM7O2IB2PAMEEJ225SXLMMPI2OTHKANFXGV4VZGCZ', 1512.3286129, '2024-03-06T22:02:21Z'], ['GAXLFHC2TPTAGAC2S66KGLOTYYBSQPC3FARZV7IT76H7EHZU4UCS4DSK', 1726.882197, '2024-03-06T22:02:21Z'], ['GCM5MCBSNRPEPRT5SZ247HP52BVTY6ZLTHZ2TF4DYWAYOUZCYR6OJXAJ', 1748.1518946, '2024-03-06T22:02:21Z'], ['GBXIYESTCD6U75KI4MJLRPHFQK6UEEJQS6GYJU7LUPXTW5BGLI7C667F', 1758.0924235, '2024-03-06T22:02:21Z'], ['GCKAXLN3LJ6Q4B3MYQ2N2TPNIBTMTCSGOA4SQAT73DAE5SWOEJGKOQB5', 1782.3881165999999, '2024-03-06T22:02:21Z'], ['GBGMHX62N5EE5LGHTRYGBYFWXK7LUYP7X46WMSG6ZSSGFADD62D2SQW2', 1784.5185332, '2024-03-06T22:02:21Z'], ['GC6CHOTYENQGRGVJUXI6OJWTZKDTGAEQFQNQDZNK7HPWMICHSJYYYHD4', 1796.3325157, '2024-03-06T22:02:21Z'], ['GBJV5XVHLBHEKWFJ26MTQRYIXLH5LMCFBOFUOLC2XLVTCORIB54OS4EA', 1798.0961682, '2024-03-06T22:02:21Z'], ['GARAPFD4GWAO3HIPSFCYXFV57K6JJSJNXWRKHNFX5GWQO2GQCKFSVOGM', 1809.3939917999999, '2024-03-06T22:02:21Z']]
  print(l_ca)
  if 1:
        delta=200
        ii=1
        num=0
        ipi=delta
        for xx in l_ca:
          num+=1
          if xx[1]>ipi:
            print(ipi-delta,"-",ipi,",",num)
            ipi+=delta
            num=0
          ii+=1
          #print("### ii,xx[1]",ii,xx[1],ipi)
  exit()
  '''

  f = open(ofile, 'w')
  ut_tm=0
  l_ca=[]
  while True:
    jd=l2dict( Nled , "")
    #Nled+=1
    pt.i_api+=1
    ###Sleep
    #last_time=SleepForAPI(Nled,last_time,flag_sleep)
    if '_embedded' in jd:
      #print(len(jd['_embedded']['records']))
      for xx in jd['_embedded']['records']:
        #print(ut_stop, xx['created_at'], date2unixtime(xx['created_at']) )
        if date2unixtime(xx['created_at']) >= ut_stop:
          print("Exited by -stop option")
          f.close()
          exit()

        type=xx['type']
        if type == 'create_account':
          ad=xx['account']
          tm=xx['created_at']
          ut_tm=date2unixtime(tm)
          bl=getMigratedBalance(ad)
          print(ad,bl,tm)
          l_ca.append([ad,bl,tm])
          f.write(ad+','+str(bl)+','+tm+"\n")

          #f.close()
          #exit()

      Nled+=1
      print("i_api",pt.i_api)
      if ut_stop < ut_tm  or pt.i_api> 10:


        #print(l_ca)
        #print(np.sort(l_ca, axis=1))
        #l_ca=sorted(l_ca, reverse=True, key=lambda x: x[1]) 
        l_ca=sorted(l_ca,               key=lambda x: x[1]) 
        print(l_ca)
        delta=200
        #ii=1
        num=0
        sum_num=0
        ipi=delta
        for xx in l_ca:
          if xx[1]>ipi:
            print("### ",ipi-delta,"-",ipi,",",num)
            f.write(str(ipi-delta)+"-"+str(ipi)+","+str(num)+"\n")
            '''
            f.write(str(ipi-delta))
            f.write('-')
            f.write(str(ipi))
            f.write(",")
            f.write(str(num))
            f.write("\n")
            '''
            ipi+=delta
            sum_num+=num
            num=0
          num+=1
          #ii+=1
        print("### ",ipi-delta,"-",ipi,",",len(l_ca)-sum_num)
        f.write(str(ipi-delta)+"-"+str(ipi)+","+str(len(l_ca)-sum_num)+"\n")
        f.close()
        exit()


    else:
      print("sleeping 5 sec....")
      time.sleep(5)

######################



def roopListEffects ( d_json , adress, ll_dummy ):
  '''
  Extract lockup information in all pages from effect tab information (dict) and address. Currently unused because there is a high possibility that only the first page has lockup information. Extracting all pages takes time because of payment information.
  '''
  l_prd=[]
  l_prdtmp=[]
  while True:
    errmsg="d_json in listEffects is NOT expected. \n adr: "+adress
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
          d_json=adr2dictE( adress , next_cs , LIM)
  return l_prd

def notRoopListEffects ( d_json , adress, ll_dummy ):
  '''
  Extract the first page lockup information from effect tab information (dict) and address.
  '''
  l_prd=[]
  l_prdtmp=[]
  next_cs , l_prdtmp= listEffects(d_json,ll_dummy)
  if len(l_prdtmp) !=0:
     l_prd.extend(l_prdtmp)
     #print(predicate)
  d_json=adr2dictE( adress , next_cs , LIM)
  return l_prd







def pList1stE ( root_adr ,l_dummy):
  if  root_adr not in l_adr_checked:
    djson=adr2dictE( root_adr , "" , LIM)
    predicate=notRoopListEffects( djson , root_adr,l_dummy )
  return predicate



def getLockInfo(adr):
  l_dummy=[]
  predicate=[]
  predicate=pList1stE(adr,l_dummy)

  #print("### DEBUG ### adr",adr)
  #print("### DEBUG ### predicate",predicate)
  #exit()


  #print("DEBUG: ", adr, predicate)

  '''
  if len(predicate) == 2:
    #print(adr,"not_locked",predicate[1],sep=',')
    return 0, predicate[1]
  else:
    if len(predicate) == 4:
      #print(adr,predicate[2],predicate[1],sep=',')
      #print(type(predicate[2]),type(predicate[1]))
      return predicate[2], predicate[1]
    else:
      print(adr,predicate[2],"error",sep=',')
      return predicate[2], "error"
  '''
  return predicate


def getPaymentsForOneAdr( adress , amth):
  pt.AMTH=amth
  l_dummy=[]
  return pt.pList1st(adress,l_dummy)



def pays2dictAdrTo ( l_pays ):

  d_adr_to={}
  adr_to=""
  adr_fr=""
  ll=[]
  #print(l_pays[0])

  for dd in l_pays:
    ll=dd.split(",")
    #print(ll)
    adr_to=ll[5]
    adr_fr=ll[3]
    #print(adr_to,adr_fr)
    if adr_to not in d_adr_to:
      d_adr_to[adr_to]=[adr_fr]
    else:
      #print(type(d_adr_to[adr_to]))
      d_adr_to[adr_to].append(adr_fr)
      #print(d_adr_to[adr_to])
  return(d_adr_to)

def getMigratedBalance(adr):
    url="https://api.mainnet.minepi.com/accounts/" + adr + "/effects"
    session = requests.Session()
    #dd = session.get(url, timeout=10)
    dd = session_get(url,session)
    jd = json.loads(dd.text)

    #print(url)
    #print(jd['_embedded']['records'])
    bla=1.0
    l_ef=jd['_embedded']['records']
    #print(len(l_ef))
    for xx in l_ef:
      #print("######################################")
      #print(xx)
      if xx['type']=='claimable_balance_claimant_created':
        bla+=float(xx['amount'])
    return(bla)

def getBalance(adr):
    url="https://api.mainnet.minepi.com/accounts/" + adr 
    session = requests.Session()
    #dd = session.get(url, timeout=10)
    dd = session_get(url,session)
    jd = json.loads(dd.text)
    balance = jd['balances'][0]['balance']
    return float(balance)


def prStolenAdrsInfoTmp (adr):
  n_to=0
  n_fr=0
  n_self=0
  ss3=0 #Number of large deposits

  #pays = getPaymentsForOneAdr(adr,200)
  # The second argument 200 means not to check less than 200π.
  pays = getPaymentsForOneAdr(adr,0)




  date_stln=""
  for pp in pays:
    ll=pp.split(",")
    date_stln=ll[7]
    adr_to=ll[5]
    adr_fr=ll[3]
    amount=float(ll[1])
    if adr_to == adr_fr:
      n_self+=1
    if adr_to==adr and adr_to!= adr_fr:
      n_to+=1
    if adr_fr==adr and adr_to!= adr_fr:
      n_fr+=1
    #if adr_to==adr and amount>AMTH:
    if adr_fr==adr and amount>AMTH:
      ss3+=1

  return n_to, n_fr, len(pays), n_self, ss3, date_stln


def prStolenAdrsInfo (shief_adr):

  d_adr_to={} # Address sending Pi to thief address
  d_adr_to=pays2dictAdrTo(getPaymentsForOneAdr(shief_adr,0))
  

  #print(d_adr_to)
  #print(shief_adr)
  #print(d_adr_to[shief_adr])

  if shief_adr not in d_adr_to  : 
    l_stolen=[]
    return l_stolen

  # aps : Adresses that the Passphrase may be Stolen
  aps=set(d_adr_to[shief_adr])

  # If there is shief_adr in aps, delete it and uniqufy
  aps_tmp=[]
  for a in aps:
    if a != shief_adr:
      aps_tmp.append(a)
    aps = set(aps_tmp)


  bla=999999.0
  #l_stolen=[["adr","n_to","n_from","n_pay","ss3","balance","lock_date","lock_period(months)"]]
  #l_stolen=[["adr","balance","date(migration)","lock_period(month)","lock_period(sec)","date(stolen)"]]
  l_stolen=[[
    "adr",
    "balance",
    "date(migration)",
    "lock_period(month)",
    "lock_period(sec)",
    "date(stolen)",
    "diff(stolen-unpend)",
    "diff(stolen-unlock)",
    ""
  ]]

  for aa in aps:
    nto, nfr, npy, nsf, ss3 , date_stolen= prStolenAdrsInfoTmp(aa)
    
    #print( aa, npy,ss3,nto,nsf,"×")
    #if (npy <= 20 and ss3== 0 and nto==0)  :
    #if  (npy <= 20             and nto==0)  :
    if  (npy <= 20             and nto==0 and date_stolen!="" )  :
    #if npy <= 10  :
      #print( aa, npy,ss3,nto,nsf,"〇")
      bla=getBalance(aa)
      s_mig=""
      s_lock=""


      #if bla<2:
      if bla<DEF_STOLEN_BALANCE:

        #print("###DEBUG npy,nto,date_stolen, aa:",npy,nto,date_stolen, aa,sep=(","))

        #s_lock, s_mig = getLockInfo(aa)
        predicate = getLockInfo(aa)
        for ii in range(0,len(predicate),2):
          #print("ii",ii)
          s_lock=predicate[ii]
          s_mig =predicate[ii+1]
          ut_mig =int(date2unixtime ( s_mig ))



          '''#######################
          ut_mig =int(date2unixtime ( s_mig ))
          ut_cancel_pend14days = ut_mig + ( 14 * 24 * 3600 )
          ut_cancel_lock       = ut_mig + s_lock
          dt_cancel_pend14days = ut2date(ut_cancel_pend14days)
          dt_cancel_lock       = ut2date(ut_cancel_lock)
          '''#########################


          
          ut_cancel_pend14days = 0
          ut_cancel_lock       = ut_mig + s_lock
          
          if ( date_stolen!= '' ):
            #df_stl_pend = date2unixtime(date_stolen) - ut_cancel_pend14days
            df_stl_pend = 0
            df_stl_ulok = date2unixtime(date_stolen) - ut_cancel_lock
          else:
            #df_stl_pend = 0 - ut_cancel_pend14days
            df_stl_pend = 0
            df_stl_ulok = 0 - ut_cancel_lock
          l_stolen.append([
            aa,
            bla,
            d2e(s_mig),
            int(s_lock/3600/24/30*10)/10,
            s_lock,
            d2e(date_stolen),
            df_stl_pend,
            df_stl_ulok
          ])



  return l_stolen

def d2e (date):
  edate = date.replace('-', '/').replace('Z', '').replace('T', ' ')
  return edate

def init_d_chd():
  '''
  d_chd={} #  dict which has been checked
  d_chd[a1]=d_prop1
       [a2]=d_prop2
       [a3]=d_prop3
        :
       [aN]=d_propN

   d_propN{
    l_atter:["shief" | "sender" | "stolen" | "unkown" | "not_check_payments"],
    l_paymens:getPaymentsForOneAdr(aN,0)

  '''

  d_chd={}

  l_a={
    'GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF',
    'GDPYUVUM6MXY5RUAWPTATGVWNT34DSTDNC3J6KGD4EAVW36XTNQALX7N',
    'GABT7EMPGNCQSZM22DIYC4FNKHUVJTXITUF6Y5HNIWPU4GA7BHT4GC5G'
  }

  for a in l_a:
    d_prop={}
    d_prop['l_atter']=['not_check_payments']
    d_prop['l_paymens']=[]
    d_chd[a]=d_prop

  return d_chd


#def traceAdrTo(a):
def traceAdr(a,mode,loota,ath):
  '''
  # 入力：aトレースアドレス ,  loota,ルートアドレス
　# 出力：入力したアドレスの履歴中送金先アドレスリスト
  #a='GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL'
  #mode:"to"
  #mode:"from"
  '''
  
  if not a in d_chd:
    d={}
    d['l_paymens']=getPaymentsForOneAdr(a,ath)
    #print(type(d['l_paymens']))
    #print(len(d['l_paymens']))
    #print(type(d['l_paymens'][-1]))
    #print(     d['l_paymens'][-1])
    #d['l_paymens'][-1]+="roota,"+loota+",mode,"+mode
    #print(     d['l_paymens'][-1])
    ii=0
    for xx in d['l_paymens']:
      d['l_paymens'][ii]+="roota,"+loota+",mode,"+mode+",ath,"+str(ath)
      ii+=1
    #print(d['l_paymens'])
    #exit()
    d_chd[a]=d
  if not a in d_chd:
    print("## DEBUG: a,",a)
    l_kara=[]
    return l_kara
  else:
    #print("ある")
    d={}
    #print(type(d_chd[a]['l_paymens']))

    if mode == "to":
      index=5
    else:
      if mode == "from":
        index=3
      else:
         print("Error unexpected mode.   mode =",mode)
         exit()
    l_ad_to=[]
    for xx in d_chd[a]['l_paymens']:
      ll=xx.split(",")
      ad_to=ll[index]
      #print(ad_to)
      l_ad_to.append(ad_to)
    #print(l_ad_to)
    l_ad_to2=list(set(l_ad_to))
    return l_ad_to2


def runTraceAdr(l_adr_to,mode,ath):
  '''
  入力：l_adr_toトレースアドレスしスト
      : mode "to" or "from"
　出力：d_chd[a]（a:トレース済アドレス、d_chd[a]['l_paymens']に履歴中送金先アドレスリストを出力
  '''
  l_loota=[]
  for aa in l_adr_to:
    l_loota.append(aa)
  #loota=l_loota[0]
    
  for a in l_adr_to:
    if a in l_loota:
      loota=a
    #l_adr_to_new = traceAdrTo(a)
    l_adr_to_new = traceAdr(a,mode,loota,ath)
    l_adr_to_tmp = []
    #print("aaaaaaaaaaaaaaaaaaaaaaaa,mode")
    for aa in l_adr_to_new:
      if a != aa :
        l_adr_to_tmp.append(aa)
    #print("type(l_adr_to_tmp)",type(l_adr_to_tmp))
    #print("type(l_adr_to)",type(l_adr_to))
    #print("a",a)
    #print("l_adr_to_tmp",l_adr_to_tmp)
    #print("len(l_adr_to)",len(l_adr_to))
    l_adr_to.extend(l_adr_to_tmp)
    l_adr_to=list(set(l_adr_to))

    print("### Napi",pt.i_api,a,mode,sep=",")
    #print("#######DEBUG ",l_adr_to)




def  prResult(odir):
  l_out=[]
  fl = [xx for xx in os.listdir(odir) if os.path.isfile(os.path.join(odir, xx))]
  for ff in fl:
    if re.match("^G.*.txt",ff):
      f = open(odir+'/'+ff, 'r')
      dl = f.read().split('\n')
      for data in dl:
        #print(data)
        l_out.append(data)
      f.close()

  f1 = open('pend3min_rep.'+odir+'.csv','w')
  f2 = open('lock3min_rep.'+odir+'.csv','w')

  lsh=[]
  ii=1
  for xxx in l_out:
    if re.match("^.*shief.*",xxx):
      ll=xxx.split(',')
      ll2=[]
      ll2.append(ll[0])
      ll2.append(ll[1])
      ll2.append(int(ll[2]))
      lsh.append(ll2)

  lsh2=[]
  lsh2=sorted(lsh, key=lambda x: x[2])
  lsh3=[]
  ii=1
  l_bar=[]
  l_barl=[]
  if len(lsh2) < 10:
    for jj in range( len(lsh2), 0, -1):
      ll=[ii]
      ll.append(lsh2[jj-1][0])
      ll.append(lsh2[jj-1][1])
      ll.append(lsh2[jj-1][2])
      lsh3.append(ll)
      ii+=1
      l_bar.append(lsh2[jj-1][2])
      l_barl.append(lsh2[jj-1][1][0]+lsh2[jj-1][1][1]+lsh2[jj-1][1][2]+lsh2[jj-1][1][3])
  else:
    for jj in range( len(lsh2), len(lsh2)-10, -1):
      ll=[ii]
      ll.append(lsh2[jj-1][0])
      ll.append(lsh2[jj-1][1])
      ll.append(lsh2[jj-1][2])
      lsh3.append(ll)
      ii+=1
      l_bar.append(lsh2[jj-1][2])
      l_barl.append(lsh2[jj-1][1][0]+lsh2[jj-1][1][1]+lsh2[jj-1][1][2]+lsh2[jj-1][1][3])
  print("\nWorst 10 addr with the most thief judgments")
  buf=""
  for ll in lsh3:
    for lll in ll:
      buf+=str(lll)
      buf+=","
    buf+="\n"
  print(buf)


  #--------------------------------


  lst=[] # list of *stolen by.*
  ii=1
  for xxx in l_out:
    if re.match("^.*shief.*",xxx):
      ll=xxx.split(',')
      adr_shf=ll[1]

    if re.match("^.*stolen by.*",xxx):
      ll=xxx.split(',')
      ll2=[]
      for ii in range(len(ll)):
        ll2.append(ll[ii])
      ll2.append(adr_shf)
      #print("#####----",ll2)
      lst.append(ll2)


  #print("\nstolen info")
  buf=""
  l_tp=[]
  l_tl=[]
  l_tpl=[]
  l_pend3min=[]
  l_lock3min=[]
  for ll in lst:
    '''
    for lll in ll:
      buf+=str(lll)
      buf+=","
    buf+="\n"
    '''

    #if (ll[1] != '0' ) and  not re.match("stolen by G", ll[1]) :
    if re.match("^[1-9]", ll[1]) :
      #print(ll)
      #print(ll[8])
      tp=float(ll[8])  #diff(stolen-unpend)
      if tp > 0 :
        l_tp.append(tp)
        l_tpl.append(tp)
        if tp < 3 * 60:
          l_pend3min.append(ll)
      tl=float(ll[9])  #diff(stolen-unlock)
      if tl > 0 :
        l_tl.append(tl)
        l_tpl.append(tl)
        if tl < 3 * 60:
          l_lock3min.append(ll)

  #print(buf)
  '''
  print(l_tl)
  print(lst[0])
  print("len(lst)",len(lst))
  print("len(l_tp)",len(l_tp))
  print("len(l_tl)",len(l_tl))
  '''
  l_np=[0,0,0]
  for xx in l_tp:
    if xx  <     3*60 :
      l_np[0] += 1
    else:
        if xx <  3*3600*24 :
          l_np[1] += 1
        else:
          l_np[2] += 1

  l_nl=[0,0,0]
  for xx in l_tl:
    if xx  <     3*60 :
      l_nl[0] += 1
    else:
        if xx <  3*3600*24 :
          l_nl[1] += 1
        else:
          l_nl[2] += 1

  l_npl=[0,0,0]
  for xx in l_tpl:
    if xx  <     3*60 :
      l_npl[0] += 1
    else:
        if xx <  3*3600*24 :
          l_npl[1] += 1
        else:
          l_npl[2] += 1

  print("len(l_np)",len(l_np))
  print("len(l_nl)",len(l_nl))
  print("len(l_npl)",len(l_npl))

  label_p=[
    "Tp < 3min.",
    "3min. <= Tp < 3day",
    "Other"
  ]

  label_l=[
    "Tl < 3min.",
    "3min. <= Tl < 3day",
    "Other"
  ]

  label_pl=[
    "Tpl < 3min.",
    "3min. <= Tpl < 3day",
    "Other"
  ]

  #x = [80, 50, 30, 20, 10]
  #plt.axis("equal")
  '''
  pie_colors = ["r", "m", "y"] 
  plt.pie(l_np, autopct='%1.1f%%', labels=label_p ,colors=pie_colors)
  #plt.savefig("l_np.jpeg")
  plt.show()
  '''

  plt.rcParams["font.size"] = 8
  pie_colors = ["r", "m", "y"] 
  fig = plt.figure()
  '''
  ax0 = fig.add_subplot(311)
  ax1 = fig.add_subplot(312)
  ax2 = fig.add_subplot(313)
  '''

  ax0 = fig.add_subplot(411)
  ax1 = fig.add_subplot(413)
  ax2 = fig.add_subplot(414)

  #ax0 = fig.add_subplot(511)
  #ax1 = fig.add_subplot(513)
  #ax2 = fig.add_subplot(514)
  #ax3 = fig.add_subplot(515)

  #  100% circle graph is num of shief
  l_bar.reverse()
  l_barl.reverse()
  ax0.set_title(odir+"\nWorst 10 addr with the most thief judgments")
  #ax0.barh(l_barl,l_bar,tick_label=l_barl,color="m")
  ax0.barh(l_barl,l_bar,                   color="m")
  s_t1 = "# of Stolen addr. By time stolen (since end of pend).  : " + str(sumLint(l_np))
  s_t2 = "# of Stolen addr. By time stolen (since lock ended) : " + str(sumLint(l_nl))
  #s_t3 = "Stolen Period between end of pend or unlock : " + str(sumLint(l_npl))
  ax1.set_title(s_t1)
  ax2.set_title(s_t2)
  #ax3.set_title(s_t3)
  ax1.pie(l_np, autopct='%1.1f%%', labels=label_p ,colors=pie_colors)
  ax2.pie(l_nl, autopct='%1.1f%%', labels=label_l ,colors=pie_colors)
  #ax3.pie(l_npl, autopct='%1.1f%%', labels=label_pl ,colors=pie_colors)
  #plt.show()
  plt.savefig(odir+".png")

  l_thf_pend3min=[]
  l_thf_lock3min=[]

  f1.write("no,thief_count,thief_adr\n")
  last_adr=l_pend3min[0][11]
  ii=0
  nn=1
  for l in l_pend3min:
    if l[11]==last_adr:
      ii+=1
    else:
      f1.write(str(nn)+','+str(ii)+','+last_adr+'\n')
      last_adr=l[11]
      nn+=1
      ii=1
  f1.write(str(nn)+','+str(ii)+','+last_adr+'\n')


  f2.write("no,thief_count,thief_adr\n")
  last_adr=l_lock3min[0][11]
  ii=0
  nn=1
  for l in l_lock3min:
    if l[11]==last_adr:
      ii+=1
    else:
      f2.write(str(nn)+','+str(ii)+','+last_adr+'\n')
      last_adr=l[11]
      nn+=1
      ii=1
  f2.write(str(nn)+','+str(ii)+','+last_adr+'\n')


  f1.write("memo,no,stolen_adr,balance,date(migration),lock_period(month),lock_period(sec),date(stolen),diff(stolen-unpend),diff(stolen-unlock),,thief_adr\n")
  for l in l_pend3min:
    for e in l:
      f1.write(e+',')
    f1.write('\n')

  f2.write("memo,no,stolen_adr,balance,date(migration),lock_period(month),lock_period(sec),date(stolen),diff(stolen-unpend),diff(stolen-unlock),,thief_adr\n")
  for l in l_lock3min:
    for e in l:
      f2.write(e+',')
    f2.write('\n')
  f1.close()
  f2.close()
  return

def sumLint(ll):
  sum=0
  for xx in ll:
    sum += xx
  return  sum

#####################
def  extMoreSpam(odir,i_unlock):
  odir_sp1 = odir + ".sp."+str(i_unlock/3600/24)+"day"
  if os.path.isdir(odir_sp1):
    shutil.rmtree(odir_sp1)
  os.mkdir(odir_sp1)


  #ut_s_dell=date2unixtime(s_del)

  l_moreSpamAdr=[]
  l_out=[]
  fl = [xx for xx in os.listdir(odir) if os.path.isfile(os.path.join(odir, xx))]
  for ff in fl:
    #print(ff)
    if re.match("^G.*.txt",ff):
      f = open(odir+'/'+ff, 'r')
      f2 = open(odir_sp1+'/'+ff, 'w')
      dl = f.read().split('\n')
      a_shiaf="xxx"
      l_stolen=[]
      f_write_stl_data=0
      for data in dl:
        ll=data.split(",")
        if(len(ll)>2) and re.match("^.*shief.*",data) :
          a_shiaf=ll[1]
          #print("shief_adr,",a_shiaf)
          s_shief_info="shief_adr,"+a_shiaf+","
          continue


        #if re.match("^stolen by G...,0,.*",data):
        if re.match("^.*adr,balance,date",data):
          #ll[1]=a_shiaf
          #s_header=ll[0]+","
          s_header=""
          for xx in ll:
            s_header+=xx+','
          #print(s_header)
          #exit()

          continue

        #if re.match("^stolen by G...,[1-9].*",data):
        if re.match("^stolen by G.*",data):
          date_stolen=ll[7]
          diff_stolen_unpend=float(ll[8])
          diff_stolen_unlock=float(ll[9])
          #print("diff_stolen_unpend,type(diff_stolen_unpend)",diff_stolen_unpend,type(diff_stolen_unpend))
          #print("diff_stolen_unlock,type(diff_stolen_unlock)",diff_stolen_unlock,type(diff_stolen_unlock))
          #print("i_unlock,type(i_unlock)",i_unlock,type(i_unlock))
          #ut_date_stolen=date2unixtime(date_stolen)
          #print("diff_stolen_unpend,i_unlock",diff_stolen_unpend,i_unlock)
          #print("diff_stolen_unlock,i_unlock",diff_stolen_unlock,i_unlock)
          #if  ut_s_dell > ut_date_stolen:
          if (diff_stolen_unpend > 0) and (diff_stolen_unpend < i_unlock):
            f_write_stl_data=1
            l_stolen.append(data)
          if (diff_stolen_unlock) > 0 and (diff_stolen_unlock < i_unlock):
            f_write_stl_data=1
            l_stolen.append(data)
          #print("ut_date_stolen",ut_date_stolen)
          #l_stolen.append(data)
          continue

        if f_write_stl_data:
          l_moreSpamAdr.append(a_shiaf)
          s_shief_info+=str(len(l_stolen))
          f2.write(s_shief_info+"\n")
          f2.write(s_header+"\n")
          for xx in l_stolen:
            f2.write(xx+"\n")
          f_write_stl_data=0

        #print("NOT deleted",data)
        f2.write(data+"\n")
      
      f.close()
      f2.close()
  f2 = open(odir_sp1+'/'+'list_sief_adr.txt', 'w')
  ii=1
  for a in l_moreSpamAdr:
    f2.write(str(ii)+","+a+"\n")
    ii+=1
  f2.close()
  print("Made MoreSpam foledr",odir_sp1)
  print("MoreSpam is detected stolen from unpend/unlock within",i_unlock)
  print("number of MoreSpam is",len(l_moreSpamAdr))

  exit()


#####################

def  delFile(odir,s_del):
  odir_d = odir + ".d"
  if os.path.isdir(odir_d):
    #print(odir_d)
    shutil.rmtree(odir_d)
  os.mkdir(odir_d)


  ut_s_dell=date2unixtime(s_del)
  #print(s_del, ut_s_dell)

  l_out=[]
  fl = [xx for xx in os.listdir(odir) if os.path.isfile(os.path.join(odir, xx))]
  for ff in fl:
    #print(ff)
    if re.match("^G.*.txt",ff):
      f = open(odir+'/'+ff, 'r')
      f2 = open(odir_d+'/'+ff, 'w')
      dl = f.read().split('\n')
      a_shiaf="xxx"
      l_stolen=[]
      f_write_stl_data=0
      for data in dl:
        ll=data.split(",")
        if(len(ll)>2) and re.match("^.*shief.*",data) :
          a_shiaf=ll[1]
          #print("shief_adr,",a_shiaf)
          s_shief_info="shief_adr,"+a_shiaf+","
          continue


        if re.match("^stolen by G...,0,.*",data):
          ll[1]=a_shiaf
          #s_header=ll[0]+","
          s_header=""
          for xx in ll:
            s_header+=xx+','

          continue

        if re.match("^stolen by G...,[1-9].*",data):
          date_stolen=ll[7]
          ut_date_stolen=date2unixtime(date_stolen)
          if  ut_s_dell > ut_date_stolen:
            #print("deleted",data)
            f_write_stl_data=1
            continue
          #print("ut_date_stolen",ut_date_stolen)
          l_stolen.append(data)
          continue

        if f_write_stl_data:
          s_shief_info+=str(len(l_stolen))
          f2.write(s_shief_info+"\n")
          f2.write(s_header+"\n")
          for xx in l_stolen:
            f2.write(xx+"\n")
          f_write_stl_data=0

        #print("NOT deleted",data)
        f2.write(data+"\n")
      
      f.close()
      f2.close()
  print("Made deleted foledr",odir_d)
  print("Deleted older than",s_del)

  exit()




def SleepForAPI(nled,last_time,flag_sleep):
  return 0

  lim=100
  sec_slp=60 * 60
  #sec_slp=60 * 30

  #sec_slp=60 * 10
  #sec_slp=60 * 5

  
  #if nled%lim < lim * 0.1 and nled//lim >last_time  :
  if pt.i_api%lim < lim * 0.1 and pt.i_api//lim >last_time  :
    flag_sleep=1
    #last_time=pt.i_api//lim
  if pt.i_api==0 and pt.i_api//lim >last_time  :
    flag_sleep=1
  if flag_sleep > 0:
    print("\n\nsleeping for SleepForAPI ",sec_slp," sec....  Napi:",pt.i_api,"  lim",lim,"    last_time:",last_time,"\n\n\n")
    time.sleep(sec_slp)
    flag_sleep=0
    last_time=pt.i_api//lim  

  '''
  lim=0 #not used
  sec_slp=60
  print("sleeping for SleepForAPI(ii) ",sec_slp," sec....  Napi:",pt.i_api,"  lim",lim,"    last_time:",last_time)
  time.sleep(sec_slp)
  '''

  return last_time


def getSpamAbleAdr(l_spam_adr,spam_score,def_lond_amo):
  l_saa=[]
  for a in l_spam_adr:
    l_saa.append([ a, spam_score])

  for spam_adr in l_spam_adr:
    ll=[]
    ll.append(getPaymentsForOneAdr(spam_adr,def_lond_amo))

    for l2 in ll:
      for l3 in l2:
        l4=l3.split(',')
        to_a=l4[5]
        if to_a != spam_adr:
          for ii in range(len(l_saa)):
            if l_saa[ii][0] == to_a:
              l_saa[ii][1]+=1
              print("to_a",to_a)
              print("l_saa[ii]",l_saa[ii])
              break
          l_saa.append([to_a,1])


  return l_saa

############################################

'''
l_adr=[
  'GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU',
  'GDISC3J222YP5DEOJ6FJQGCRLRA2R3FFZPCTREXGQNUXWGGPNJ5AQG27',
  'GARKPUF7VEI7EDNXIVUGIMSXN5TJKTAKH3J3LF2E7HTZQJWB6SKE4M4L',
  'GDIZUA3WX2AOOIR3VUE2NU357JJTZEAFR5P6VGK6KEWDP766ZV6CIRRB'
]
'''


















'''
## dev. code -> pending

##################
d_chd=init_d_chd()
##################
l_adr_to=[
  'GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL',
  'GAFYXHBXYNDLKLZXBZSR6MLCNA4QJ4CPT3NDPV56AU5BIGGZ7CJOWRZ5'
]
runTraceAdrTo(l_adr_to)
for k in d_chd:
  print("key: ",k,len(d_chd[k]['l_paymens']))

print("#### abcabc ABC ######")

exit()


l_shief_adr=[
  'GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL',
  #'GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU',
  #'GAFYXHBXYNDLKLZXBZSR6MLCNA4QJ4CPT3NDPV56AU5BIGGZ7CJOWRZ5',
  #'GC3ZUA5QA6E4GWF5SMK2IWRDTWPFAO3QFXUWT3MH6PQAN3PUJW22UHSA',
]

for shief_adr in l_shief_adr:
  print("shief_adr,"+shief_adr)
  l_stolen=prStolenAdrsInfo (shief_adr)

  ii=0
  for xxx in l_stolen:
    #print(ii,xxx, sep=',')
    buf = str(ii) + ","
    for xx in xxx:
      buf += str(xx) + ","
    print(buf)
    ii+=1
print("")

'''







print("########")


'''
l_ck=['x','y','z']
##################
odir="out"
if not os.path.isdir(odir):
  os.mkdir(odir)
files = os.listdir(odir)
for s in files:
  s = re.sub('\.txt$', '', s)
  l_ck.append(s)
##################
print(l_ck)
exit()
'''




'''
aa="GC4IQM7SA2OTTQJSWJFJ6TVIVGHLTWNR7ULRD2TF7BZJAFZ3CJGDDHQN"
a,b,c,d,e,f=prStolenAdrsInfoTmp(aa)
print(f,d2e(f))
exit()
'''


'''
shief_adr="GCYGA2GHSEXGEWY5AO7JPAJZGKKCSZNAOOTHBXQDCUR6RWT7666IXBKX"
shief_adr="GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL"
shief_adr="GAF2NORU42L47Z5T2HMCZ7SEX755GFUCJXVI4M2EIXX7JS3V43GJ4RPP"
#print("running getstolen_name",shief_adr)
getstolen_name (shief_adr)
exit()
'''



'''
f = open('GBU7.adr.txt', 'r')
dl=f.readlines()
f.close()
dl=[ii.replace("\n", "") for ii in dl]
for ii in dl:
  if ii[0] == 'G' and len(ii)==56:
    print("### running getstolen_name ... ",ii)
    getstolen_name(ii)
exit()
'''

'''
aa='GBU7PR3VSIWZGQZYOHP6KEUEBJPX4HYN6FMHDB5VQNJ2NNVCWU4D5ANE'
ll=getPaymentsForOneAdr(aa,0)
for xx in ll:
  print(xx)
exit()
'''


'''
print("###test#####")

l_shief_adr=[
    'GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL',
    'GCM4U4H5XUYET3WBJIKBG26RQQ7NLVJNTK6O5Y6NQYHXLWTUH53R5DQF',
    'GA4I7K6Q7P22VV6ATKU2JPNRHYYI5H5JHFM52CF5UX6VCCCBMTNSREF3',
    'GBC4FTWNWWIMMURYTKWLHIT22MXJXQIH3NJCBYLDJFLLCSQ6RAHTDDA6',
    'GAOZM6OMT6QS75TGJEJHRJU7VQMWDOPRPD43EXN5YQTKTSQXSDQD6V5Z',
    #'GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU',
]

for sa in l_shief_adr:
  getstolen_name(sa)
exit()
'''






print("###test3#####")

path="spam_adr.txt"
with open(path) as f:
  s = f.read()
l_sa=s.split("\n")
f.close()
l=getSpamAbleAdr(l_sa,1000,100)
for x in l:
  #print(x)


'''
v3.10はこれ使って複数ロックアップを扱えるようにする
https://api.mainnet.minepi.com/accounts/GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW/effects?type=claimable_balance_claimant_created?limit=200
'''

'''
sa="GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL" #stole suzuki 
f = open(sa[0]+sa[1]+sa[2]+sa[3]+".th_"+str(DEF_STOLEN_BALANCE)+".csv", 'w')
getstolen_name(sa,f)
print("### Napi",pt.i_api,sep=",")
f.close()
exit()
'''

#----
'''
sa="GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW" #seo
sa="GCKW52W4TGB7JFMTH6HK5QFBPYGSOGRZK5ZHOLQNW53FUJCCK2M5FJ4R" #suzuki
a=getLockInfo(sa)
print("### getLockInfo ###", a)
sa="GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL" #stole suzuki
b=prStolenAdrsInfo(sa)
print("### prStolenAdrsInfo ###")
for xx in b:
  print(xx)
exit()
'''

'''
DEF_STOLEN_BALANCE=2
#DEF_STOLEN_BALANCE=10
sa="GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW" #seo
sa="GCKW52W4TGB7JFMTH6HK5QFBPYGSOGRZK5ZHOLQNW53FUJCCK2M5FJ4R" #suzuki
sa="GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL" #stole suzuki 
f = open(sa[0]+sa[1]+sa[2]+sa[3]+".th_"+str(DEF_STOLEN_BALANCE)+".csv", 'w')
getstolen_name(sa,f)
print("### Napi",pt.i_api,sep=",")
f.close()
exit()
'''





'''
#現実逃避　198枚（ロックアップ９０％）　195枚盗まれるyouko0707 GCWU～　4/27 22:29 コメントを探すcode

blk=14413140 # 4/27 22:31, 2024
blk=14409700 # ここまでチェック済
blk=14390300 # ここまでチェック済
blk=14340400 # ここまでチェック済
blk=14328300

cdwn=50000 #500で９分
blk_e=blk-cdwn

for ii in range(blk,blk_e,-1):
  if ii%100 == 0 :
    print("### blk no",ii,"###")
  url="https://api.mainnet.minepi.com/ledgers/"+str(ii)+"/operations"
  session = requests.Session()
  dd = session_get(url,session)
  jd = json.loads(dd.text)
  ll=jd['_embedded']['records']
  for xx in ll:
    if xx['type']=='claim_claimable_balance':
      adr=xx['source_account']
      #print('source_account',adr)
      adr4=adr[0]+adr[1]+adr[2]+adr[3]
      #print(adr4)
      mb=getMigratedBalance(adr)
      gp=getPaymentsForOneAdr(adr,0)
      lp=[]
      for pp in gp:
        lp_elm=[]
        lpp=pp.split(',')
        amo=float(lpp[1])
        fra=lpp[3]
        toa=lpp[5]
        if fra == adr :
          lp_elm.append(amo)
          lp_elm.append(toa)
          lp.append(lp_elm)
      #if adr4 == "GCWU" :
      #  print("GCWU found!")
      if len(lp)>0 and mb < 1990 and mb > 1970:
        print("### blk no",ii,"###")
        print('source_account',adr4,adr)
        print("migrated_balance",mb)
        for lpp in lp:
          toa=lpp[1]
          toa4=toa[0]+toa[1]+toa[2]+toa[3]
          print( lpp[0] ,"sent to",toa4,toa)
        #exit()
exit()
'''



'''
sa='GB4ENRZDND4GW2VXPSEXYPCLPDDKYYK3S6MJCIVVGUY5O5QPW7PUHJ65'
f = open("GB4E_vtnm_shief.csv", 'w')
getstolen_name(sa,f)
print("### Napi",pt.i_api,sep=",")
f.close()
exit()
'''

'''
a=['stolen by GA22', 'stolen by GA22', 'GA22ZID2EQGXTGSSAEZO6ZRHJRWJ4TLDKT2XCIXXHICEDJJVVIAKZTDY', 'adr', 'balance', 'date(migration)', 'lock_period(month)', 'lock_period(sec)', 'date(stolen)', 'diff(stolen-unpend)', 'diff(stolen-unlock)', '', '', '']

if a[1]!= '0' or re.match("^stolen by G.*",a[1]):
  print("OK")
else:
  print("ng")

exit()
'''




'''
#11/1 UTC 0:00 https://api.mainnet.minepi.com/ledgers/11477720

#n_st=11477720 - 17280
n_st=11461295 # 10/30 0:00 UTC


#n_chk = int(30  * 3600 / 5)
#n_chk = int(3*24  * 3600 / 5) # 51280
n_chk = 50000
#n_chk = 30

#n_ofs =       3 * 3600 / 5
n_ofs =       0
n_sto = int( n_st - n_ofs )


l_chk=[
  "operation_count",
  "tx_set_operation_count",
  "closed_at",
  "sequence"
]
buf="time,"
for xx in l_chk:
  buf+=xx+","
print(buf)
for ii in range(n_sto, n_sto+n_chk):
  jd=l2dict2( ii  )
  buf=str(int((date2unixtime(jd["closed_at"])))) + ","
  buf=str(ut2date(int((date2unixtime(jd["closed_at"]))))) + ","
  for xx in l_chk:
    buf+=str(jd[xx])+","
  print(buf)
exit()
'''


'''
#a_pb="GAMLE6AGRJ6T7WCJGLXVUPQKIAUAKXLHMAVM7FLD25ODMY7QJJ6JCEXB"
a_pb="GASPIWETKPXRSC7JI2QCAOIYFRM4T7T42XNZS6BQW6WLPIFWNJZIXLHJ"
pays = getPaymentsForOneAdr(a_pb,0)
#print(pays)
print(len(pays))
print("a_pb",a_pb,sep=",")
for pp in pays:
  ll=pp.split(",")
  buf=""
  for xx in ll:
    buf += xx+","
  print(buf)
exit()
'''




'''
pt.f_mode = 0 #0;to 1:from 2:to&from
pt.AMTH=1000

d_pays={}
ra='GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU'
ra='GBVUVER2V4F5G2CADBIN3OUA3BGC3QMGP64PRBLCM7PBJFWFSX7J7TE7'
l_l_adr_may_not_checked=[]
d_pays=pt.pList(ra,l_l_adr_may_not_checked)
pt.monSum ()
print("num of api:",pt.i_api)

ii=1
for k ,v in d_pays.items():
  print(ii,k,v)
  ii+=1
exit()
'''

'''
#トレースv3 ←v2より情報少ない。なんでだ？
##################
d_chd=init_d_chd()
##################
f = open("tmp.csv", 'w')
#print("### Napi",pt.i_api,sep=",")

#mode = "from"
mode = "to"
ath=1000

l_adr_to=[
  'GDS73TBQ5L2KX2D7EWMY43O4NB3RZXE4XFTH6SBRZK3QZJCB2L63GQHU',
  #'GCYNLXQNGK4PWXYNJLOUGQGGCCF5BTXHFLMXOUH3EKYM6L3MSU6YRU6B',
  #'GCDPBIDI6GSHKXGHALMFH2BGYQNFPRDFVSIDHCESTIQSG5E7UJ3PMPO7',
  #'GAMS6JIZ7YGLGGW7XTOZC5KPZAIVAXEILSGW4K42HCHAECZFR6N5ELF2',
  #'GC7TSDOYNGZJG2DLVM3H4V3ODY4G44KO3LMIOJ6DFDTKZWEOAXC3OVUK',
  #'GDNP3JOFE2EZMDACJ7IVWEWGEUG7W6UPMGAKPTUDFT5MTAWJ34J2CJ4S',
  #'GB24EDOH5KMLR2QHJBHMO4VCLEXKESCR3S6HVWYA4KVCUJB5KGP4TI53',
  #'GDGEOJDCYENKMRP7RHFNHBG3KARO7QFD4D5H5HKIREHBBVFFSAGV2QYI',
  #'GDG43JL4PY3TDJKQDCIET65QIHJJ3XED5GU6CP5RENU2UGM4EQ6LML33',
  #'GDK6TV2QRYD4A77FTGG7BWNOYXNZV74QS23Z6PCXK67IZALOAWSP2EHL',
  #'GBVUVER2V4F5G2CADBIN3OUA3BGC3QMGP64PRBLCM7PBJFWFSX7J7TE7',

]
runTraceAdr(l_adr_to,mode,ath)

l_trc=[]
buft=""
for k in d_chd:
  buft+=str(len(d_chd[k]['l_paymens']))
  buft+=","
  buft+=k
  buft+=","
  buft+="mode"
  buft+=","
  buft+=str(mode)
  buft+=","
  buft+="ath"
  buft+=","
  buft+=str(ath)
  l_trc.append(buft)
  buft=""
  for ll in d_chd[k]['l_paymens']:
    f.write(ll+"\n")

ii=1
for xx in l_trc:
  print(ii,xx)
  f.write(str(ii)+xx+"\n")
  ii+=1

print("#### abcabc ABC ######")
f.close()
exit()
'''









'''
ut=1
if 1698764400.0 > ut:
  print("True")
else:
  print("False")
exit()
'''



args = sys.argv

ut_stop=9999999999999999
for ii in range(len(args)):
  if args[ii] == "-blk" or args[ii] == "-b":
    for jj in range(len(args)):
      if args[jj] == "-stop":
        ut_stop = date2unixtime(args[jj+1] +" 00:00:00")  #yyyy/mm/dd
        #ut_stop -= 9 * 3600 #UTC+9

    for jj in range(len(args)):
      if args[jj] == "-o":
        odir = args[jj+1]
        if args[ii] == "-blk":
          Nled=int(args[ii+1])
        if args[ii] == "-b":
          url="https://api.mainnet.minepi.com/"
          session = requests.Session()
          #dd = session.get(url, timeout=10)
          dd = session_get(url,session)
          jd = json.loads(dd.text)
          core_latest_ledger = jd['core_latest_ledger']
          #print(type(core_latest_ledger))
          Nled=core_latest_ledger
        l_ck=[
          'GDGVILYX4RATPIO6XTBXNIBEUZXI3EBI36NJXKGO4DVJINYJ5X42WXHF',   #PCM
          'GDUPXUGENG2YCX4BVYKS3LH4N4UT7BTYPMBOS5UCVTAX2E5IZ6VYLC4L',   #PCM
          'GBQQRIQKS7XLMWTTRM2EPMTRLPUGQJDLEKCGNDIFGTBZG4GL5CHHJI25',  #CT
          'GDPDSLFVGEPX6FJKGZXSTJCPTSKKAI4KBHBAQCCKQDXISW3S5SJ6MGMS',  #CT
          'GB7HLN74IIY6PENSHHBBJJXWV6IZQDELTBZNXXORDGTL75O4KC5CUXEV',  #CT
          'GBU7PR3VSIWZGQZYOHP6KEUEBJPX4HYN6FMHDB5VQNJ2NNVCWU4D5ANE',  #teltlk
        ]
        Run_getstolen_name( Nled , odir, ut_stop)

    for jj in range(len(args)):
      if args[jj] == "-omig":
        #odir = args[jj+1]
        ofile = args[jj+1]
        if args[ii] == "-blk":
          Nled=int(args[ii+1])
        if args[ii] == "-b":
          url="https://api.mainnet.minepi.com/"
          session = requests.Session()
          #dd = session.get(url, timeout=10)
          dd = session_get(url,session)
          jd = json.loads(dd.text)
          core_latest_ledger = jd['core_latest_ledger']
          #print(type(core_latest_ledger))
          Nled=core_latest_ledger
        #Run_getstolen_name( Nled , odir, ut_stop)
        Run_getsMigBlance( Nled , ofile, ut_stop)

    print("'-o' or '-omig' option Not found for '-blk' or '-b'")
    exit()




  if args[ii] == "-plot":
    for jj in range(len(args)):
      if args[jj] == "-o":
        odir = args[jj+1]
        prResult(odir)
        exit()


  if args[ii] == "-d":
    for jj in range(len(args)):
      if args[jj] == "-d":
        s_del = args[jj+1] +" 00:00:00"  #yyyy/mm/dd
        for kk in range(len(args)):
          if args[kk] == "-o":
            odir = args[kk+1]
            delFile(odir,s_del)
            exit()

  if args[ii] == "-sp":
    for jj in range(len(args)):
      if args[jj] == "-sp":
        i_unlock = float(args[jj+1])  # [sec]
        for kk in range(len(args)):
          if args[kk] == "-o":
            odir = args[kk+1]
            extMoreSpam(odir,i_unlock)
            exit()


  if args[ii] == "-sa":
        sa=args[ii+1]
        f = open(sa[0]+sa[1]+sa[2]+sa[3]+".csv", 'w')
        getstolen_name(sa,f)
        print("### Napi",pt.i_api,sep=",")
        f.close()



