from jsonrpcclient import request, parse, Ok
import logging
import requests
#Program description
#This program exists to monitor the attacker and it's transactions.  This program needs to query the blockchain and each transaction for each address.
  
#Variables
intCurrBlock = 0
strRpcAddr = 'http://<RPC Username Here>:<RPC Password Here>@<RPC IP Here>:<RPC Port Here>/'

def GetBlockCount():
    response = requests.post(strRpcAddr, json=request("getblockcount"))
    #print(response)
    return ParseResponse(response)

def GetEntireChain(intCurrBlockNum):
    dictBlockchainInfo = {}
    for intCounter in range(intCurrBlockNum):        
        respGetBlkHash = requests.post(strRpcAddr, json=request("getblockhash", params=(intCounter,))) 
        strCurrBlockHash = ParseResponse(respGetBlkHash)       
        respCurrBlock = requests.post(strRpcAddr, json=request("getblock", params=(str(strCurrBlockHash), True,)))
        dictBlockchainInfo[strCurrBlockHash] = ParseResponse(respCurrBlock)
        print("Curr block hash: " + str(strCurrBlockHash) + "---" + "Block Info: " + str(dictBlockchainInfo[strCurrBlockHash]))
    return dictBlockchainInfo

def GetSpecifiedBlockHash(intBlockNum):
    print(intBlockNum)
    response = requests.post(strRpcAddr, json=request("getblockhash", params=(intBlockNum,)))
    return ParseResponse(response)
    
def ParseResponse(pResponse):
    parsed = parse(pResponse.json())
    if isinstance(parsed, Ok):
        return parsed.result
    else:
        return logging.error(parsed.message)

def SendCommandNoParams(strCommand):
    response = requests.post(strRpcAddr, json=request(strCommand))
    return ParseResponse(response)
    
def SendCommandWithParams(strCommand, param1):
    response = requests.post(strRpcAddr, json=request(strCommand, params=(param1,)))
    return ParseResponse(response)

#First, get the block count
BlockCount = GetBlockCount()
print("The block count is: " + str(BlockCount))
CurrBlockHash = GetSpecifiedBlockHash(BlockCount)
print("GetSpecifiedBlockHash() output is: " + str(CurrBlockHash))
EntireChain = GetEntireChain(BlockCount)
print(SendCommandWithParams("help", "getblock"))
