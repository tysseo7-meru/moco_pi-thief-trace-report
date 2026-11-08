
import sys
import piTracePayments_lib as pt
l_adr_may_not_checked=[]

args = sys.argv
root_adr    = str(args[1])
ii=0
for xxx in args:
  if xxx=="-to":
    if pt.f_mode==2:
      pt.f_mode = 0
    else:
      pt.f_mode = 1
  if xxx=="-from":
    if pt.f_mode==1:
      pt.f_mode = 0
    else:
      pt.f_mode = 2
  if xxx=="-ath":
    if ii == len(args) - 1 :
      print("Error: -ath value is not specify")
      exit()
    v_ath = float(args[ii+1])
    if not isinstance(v_ath, (int, float)):
      print("Error: -ath value must be number. you spesify value of ath =",v_ath)
      exit()
    else:
      pt.AMTH=v_ath
  ii=ii+1


######### main ##########



pt.pList ( root_adr, l_adr_may_not_checked )
pt.monSum ()
print("num of api:",pt.i_api)


'''
ii=0
for a in pt.l_adr_checked:
  ii+=1
  print(ii,a)
print("len(l_adr_checked) ",len(pt.l_adr_checked))

print("############# d_adr_recv ##########")
#print(pt.d_adr_recv)
ii=0
for k in list(pt.d_adr_recv.keys()):
  ii+=1
  print(ii,k, pt.d_adr_recv[k])
print("############# d_adr_send ##########")
print(pt.d_adr_send)
ii=0
for k in list(pt.d_adr_send.keys()):
  ii+=1
  print(ii,k, pt.d_adr_send[k])
'''