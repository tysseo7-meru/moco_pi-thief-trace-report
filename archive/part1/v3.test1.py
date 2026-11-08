import v3_11 as v3

'''#############
#a="GDVWOYCULBEYT7TKGZKAO5R4HDOL3MNTJLB2MXZ76CQNUF6KN4HHHMAW" #seo
#a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW" #test shief
a="GCEXIRDHTESXA7ZXZDTS5L7XWTVJOKGACKHURKLI2CYXWQ6E22TWFILW"
#l=v3.getPaymentsForOneAdr(a,0)
l=v3.getPaymentsForOneAdr(a,48)
for xx in l:
  print(xx)
'''############

path="from_GING.txt"
with open(path) as f:
  s = f.read()
lg=s.split("\n")
f.close()

for aa in lg:
  print(aa[0]+aa[1]+aa[2]+aa[3]+aa[4],aa)

#VTH=48
#VTH=99
VTH=999
print("### VTH",VTH)


dg={}
ddb={}
#for ii in range(3):
for ii in range(len(lg)):
  print("###",lg[ii])
  l1=v3.getPaymentsForOneAdr(lg[ii],VTH)
  for xx in l1:
    #print("org_data",xx)
    ltmp=[]
    if lg[ii] in ddb:
      ltmp=ddb[lg[ii]]
      ltmp.append(xx)
      ddb[lg[ii]]=ltmp
    else:
      ltmp.append(xx)
      ddb[lg[ii]]=ltmp
    #print(yy[2],yy[3]) #from
    #print(yy[4],yy[5]) #to
    #print(yy[0],yy[1]) #ammount
  for xx in l1:
      yy=xx.split(",")
      if lg[ii]==yy[3] :   # from(lg[ii]) --> to
        sdir='out'
      else:                # from         --> to(lg[ii])
        sdir='in'
      dtmp={}
      ltmp=[]
      if lg[ii] not in dg:
        ltmp.append(yy[5])
        dtmp[sdir]=ltmp
        dg[lg[ii]] = dtmp
      else:
        if sdir in dg[lg[ii]]:
          ltmp=dg[lg[ii]][sdir]
          if yy[5] not in dg[lg[ii]][sdir]:
            ltmp.append(yy[5])
            dg[lg[ii]][sdir]=ltmp
        else:
          ltmp.append(yy[5])
          dg[lg[ii]][sdir]=ltmp




print("### ddb ###")
#print(ddb)
print("### dg ###")
print(dg)

print("###### dg in/out ######")
for k in dg:
  a4=k[0]+k[1]+k[2]+k[3]
  a4_in_num = len(dg[k]['in'])
  a4_out_num= len(dg[k]['out'])
  print(a4,"a4_in_num",a4_in_num,"a4_out_num",a4_out_num)



exit()


