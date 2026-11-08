# coding:utf-8

#==========================
# インポートモジュール
#==========================
import urllib.request
import json
import socket
import time
import sys

#==========================
# グローバル変数
#==========================
args = sys.argv
PROXY_LIST_URL = 'https://www.proxyscan.io/api/proxy'

#==========================
# 関数
#==========================

## プロキシリストをJSON形式で取得する
# (ex)https://www.proxyscan.io/api/proxy?last_check=9800&uptime=50&ping=500&limit=10&type=https
def getProxyJson(_type):
  # 引数が正しいかどうかのチェック
  if _type != 'http' and _type != 'https':
    print('Args Error.')
    return []
  
  apiUrl = PROXY_LIST_URL + '?last_check=3600&uptime=75&limit=10&type=' + _type + '&ping='
  
  # ping を段階的に上げていく。もし1つでも返ったらbreak
  for i in range(4):
    pingCount = str((i + 1) * 300)
    reqApi = apiUrl + pingCount
    print(reqApi )
    with urllib.request.urlopen(reqApi) as res:
      j = res.read().decode('utf-8')
      resJson = json.loads(j)
      if len(resJson) != 0:
        return resJson
      else:
        print('Pxy is Null.')
        continue
    
    time.sleep(10)
 # あんまり連続でアクセスすると攻撃っぽくなるのでSleep処理

## プロキシが正常に使用できるかをチェックする
def checkServerPort(_ip, _port):
  ipAddr = _ip
  port = _port
  print('Port Check pxy... [IPADDR]' + ipAddr + ' [PORT]' + str(port))
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10) # タイムアウトの指定
  return_code = sock.connect_ex((ipAddr, port))
  sock.close()
  
  # もしきちんと空いているならTrueを返す
  if return_code == 0:
    print('[OK]', ipAddr + ':' + str(port))
    return True
  else:
    print('[NG]', ipAddr + ':' + str(port))
    return False

## プロキシリストを返却する
#PROXIES = {
#  'http': 'http://100.0.0.1:80',
#  'https': 'https://100.0.0.2:3128'
#} って言う感じの辞書型
def getProxyList():
  resProxies = {}
  httpJsons = getProxyJson('http')
  for httpjs in httpJsons:
    ipAddr = httpjs['Ip']
    port = httpjs['Port']
    
    # もしきちんと空いているなら辞書型変数に追加
    if checkServerPort(ipAddr, port):
      resProxies['http'] = 'http://' + ipAddr + ':' + str(port)
      break
  
  httpsJsons = getProxyJson('https')
  for httpsjs in httpsJsons:
    ipAddr = httpsjs['Ip']
    port = httpsjs['Port']
    
    # もしきちんと空いているなら辞書型変数に追加
    if checkServerPort(ipAddr, port):
      resProxies['https'] = 'https://' + ipAddr + ':' + str(port)
      break
  
  return resProxies

#==========================

print(getProxyList())


