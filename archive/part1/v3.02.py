#### python -m pip install --upgrade pip setuptools
#### pip install requests
#### pip install simplejson


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
import piTracePayments_lib2 as pt


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
  url = "https://api.mainnet.minepi.com/accounts/" + addr + "/effects?cursor=" +  str(cursor) + "&limit=" + str(limit) +"&order=asc"
  session = requests.Session()
  dd = session.get(url)
  jd = json.loads(dd.text)
  return jd



def l2dict( ledger , cursor ):

  #ll=[]
  #print(addr)
  url = "https://api.mainnet.minepi.com/ledgers/" + str(ledger) + "/operations??cursor=" +  str(cursor) + "&limit=200"
  session = requests.Session()
  dd = session.get(url)
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



def Run_getstolen_name( Nled , odir):
  #odir="out"
  if not os.path.isdir(odir):
    os.mkdir(odir)
  files = os.listdir(odir)
  for s in files:
    s = re.sub('\.txt$', '', s)
    l_ck.append(s)

  while True:
    jd=l2dict( Nled , "")
    if '_embedded' in jd:
      for xx in jd['_embedded']['records']:
        type=xx['type']
        if type == 'payment':
          amo = float(xx['amount'])
          frm = xx['from']
          print(Nled,amo,frm)
          if amo>98 and (frm not in l_ck):
            #print("#####getstolen_name####",frm)
            ofile = odir + '/' + frm + '.txt'
            f = open(ofile, 'w')
            dt_now = datetime.datetime.now()
            ut_s=int(date2unixtime(str(dt_now.strftime('%Y-%m-%d %H:%M:%S'))))
            f.write("Strat,"+str(dt_now))
            f.write("\n")
            getstolen_name(frm,f)
            l_ck.append(frm)
            dt_now = datetime.datetime.now()
            ut_e=int(date2unixtime(str(dt_now.strftime('%Y-%m-%d %H:%M:%S'))))
            f.write("\nEnd,"+str(dt_now))
            f.write("\nRunTime,"+str(ut_e-ut_s)+",sec")
            f.write("\n")
            f.close()
    Nled+=1







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


  #print("DEBUG: ", adr, predicate)

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


def getPaymentsForOneAdr( adress , amth):
  pt.AMTH=amth
  l_dummy=[]
  return pt.pList1st(adress,l_dummy)

  '''
  l_pays_tmp=[]
  l_pays=[]
  d_json={}
  next_cs=""

  d_json=pt.adr2dict( adress , "" , LIM)
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
          d_json=pt.adr2dict( adress , next_cs , LIM)
          next_cs , l_pays_tmp = pt.listPayments(d_json,l_dummy)
          l_pays.extend(l_pays_tmp)
          d_json=pt.adr2dict( adress , next_cs , LIM)
    return(l_pays)
  '''

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


def getBalance(adr):
    url="https://api.mainnet.minepi.com/accounts/" + adr 
    session = requests.Session()
    dd = session.get(url)
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


      if bla<2:

        print("###DEBUG npy,nto,date_stolen, aa:",npy,nto,date_stolen, aa,sep=(","))

        s_lock, s_mig = getLockInfo(aa)
        ut_mig =int(date2unixtime ( s_mig ))
        ut_cancel_pend14days = ut_mig + ( 14 * 24 * 3600 )
        ut_cancel_lock       = ut_mig + s_lock
        dt_cancel_pend14days = ut2date(ut_cancel_pend14days)
        dt_cancel_lock       = ut2date(ut_cancel_lock)

        if ( date_stolen!= '' ):
          df_stl_pend = date2unixtime(date_stolen) - ut_cancel_pend14days
          df_stl_ulok = date2unixtime(date_stolen) - ut_cancel_lock
        else:
          df_stl_pend = 0 - ut_cancel_pend14days
          df_stl_ulok = 0 - ut_cancel_lock
        #l_stolen.append([aa,nto,nfr,npy,ss3,bla,s_mig,int(s_lock/3600/24/30*10)/10])
        #l_stolen.append([aa,bla,d2e(s_mig),int(s_lock/3600/24/30*10)/10,d2e(date_stolen)])
        #l_stolen.append([aa,bla,d2e(s_mig),int(s_lock/3600/24/30*10)/10,s_lock,d2e(date_stolen)])
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


def traceAdrTo(a):
  '''
  # 入力：アドレス a
　# 出力：入力したアドレスの履歴中送金先アドレスリスト
  #a='GAJ4MHYDFYZBBTRR53L43NUEVMTTOD5DHBKBUO6Q64HJGVWDRTKVKSUL'
  '''
  if not a in d_chd:
    d={}
    d['l_paymens']=getPaymentsForOneAdr(a,0)
    d_chd[a]=d
  if not a in d_chd:
    print("## DEBUG: a,",a)
    l_kara=[]
    return l_kara
  else:
    #print("ある")
    d={}
    #print(type(d_chd[a]['l_paymens']))
    l_ad_to=[]
    for xx in d_chd[a]['l_paymens']:
      ll=xx.split(",")
      ad_to=ll[5]
      #print(ad_to)
      l_ad_to.append(ad_to)
    #print(l_ad_to)
    l_ad_to2=list(set(l_ad_to))
    return l_ad_to2


def runTraceAdrTo(l_adr_to):
  '''
  入力：l_adr_toトレースアドレスしスト
　出力：d_chd[a]（a:トレース済アドレス、d_chd[a]['l_paymens']に履歴中送金先アドレスリストを出力
  '''
  for a in l_adr_to:
    l_adr_to_new = traceAdrTo(a)
    l_adr_to_tmp = []
    #print("aaaaaaaaaaaaaaaaaaaaaaaa")
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








print("###test2#####")



args = sys.argv
for ii in range(len(args)):
  if args[ii] == "-blk":
    #print("found '-blk'")
    #print("found '-blk' arg is",args[ii+1],type(args[ii+1]))
    for jj in range(len(args)):
      if args[jj] == "-o":
        odir = args[jj+1]
        Nled=int(args[ii+1])
        l_ck=[]
        Run_getstolen_name( Nled , odir)
    print("'-o' option Not found for '-blk'")
    exit()


