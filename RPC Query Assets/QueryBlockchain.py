from jsonrpcclient import request, parse, Ok
import logging
import requests
import pymongo
import json

#Program description
#This program exists to monitor the attacker and its transactions.  This program needs to query the blockchain and each transaction for each address.

#Variables
intCurrBlock = 0
#strRpcAddr = 'http://<RPC Username Here>:<RPC Password Here>@<RPC IP Here>:<RPC Port Here>/'
dictMenuOptions = dict()

#Classes
class Transaction:
    def __init__(self):
        self.Hash = ''
        self.Sender = ''
        self.Recipient = ''
        self.Amount = 0



class Block:
    def __init__(self, pHash, pBlockNum):
        self.BlockNum = pBlockNum
        self.Hash = pHash
        #An empty tuple
        self.TXs = ()


    def AddTx(self, pTransaction):
        self.TXs = self.TXs + (pTransaction,)


#Functions
def GetSpecifiedBlockHash(intBlockNum):
    return SendCommand("getblockhash", (intBlockNum,))
    
def GetBlockCount():
    return SendCommand("getblockcount")
    
def GetRawTx(pTxId):
    return SendCommand("getrawtransaction", (pTxId, True,))
    
def GetBlockInfo(pBlockHash):
    return SendCommand("getblock", (pBlockHash, True))  
    
def ParseTxIdsDataFromGetBlock(pGetBlockResp):
    lstTxIds = pGetBlockResp["tx"]
    return lstTxIds
    
def ParseResponse(pResponse):
    parsed = parse(pResponse.json())
    if isinstance(parsed, Ok):
        return parsed.result
    else:
        return logging.error(parsed.message)

def GetHelpText(strCommand):
    return SendCommand(strRpc1Addr, "help", (strCommand,))
    
def SendCommand(strMachine, strCommand, pParams = ()):
    response = requests.post(strMachine, json=request(strCommand, params = pParams)) 
    return ParseResponse(response)

#Get chain info from genesis to specified block number
def GetChainFromGenTo(intBlockNum):
    tupBlockchainInfo = ()
    for intCounter in range(12587, intBlockNum + 1):  
        #Get block hash of specified block number      
        strCurrBlockHash = GetSpecifiedBlockHash(intCounter) 
        objBlock = Block(strCurrBlockHash, intCounter) 
        #Get block info of specified block hash     
        lstCurrBlockInfo = GetBlockInfo(strCurrBlockHash)
        #Parse out transactions in from block info
        lstTxData = ParseTxIdsDataFromGetBlock(lstCurrBlockInfo)
        #Add to block hash transaction information to dictionary as a kvp 
        for x in lstTxData:
            objNewTx = Transaction()
            objNewTx.Hash = x
            objBlock.AddTx(objNewTx)
        tupBlockchainInfo = tupBlockchainInfo + (objBlock,)
    return tupBlockchainInfo

def GetTxInfo(pTxId):
   return SendCommand("getrawtransaction", (pTxId, 1,))

def IsMintTx(lstInputVals):
    #only one array element and there is no prevout element then it's a mint transaction
    if len(lstInputVals) == 1 and "prevout" not in lstInputVals:
        return True
    else:
        return False

# #Main body
# print("***Welcome to Testcoin Query Tool***")
# while True:
#     try:
#         strInput = input("What would you like to do?")
#         if strInput == "H":
#             print("H entered")
#         else:
#             print("Else block")
#     except KeyboardInterrupt:
#         print("\nCRTL + C received, shutting down right now.")
#         break

# #First, get the block count
# BlockCount = GetBlockCount()
# print("Curr Block Count: " + str(BlockCount))
# CurrBlockHash = GetSpecifiedBlockHash(BlockCount)
# print("Curr Block Hash: " + str(CurrBlockHash))
# print(GetSpecifiedBlockHash(12595))

# #We really want the entire chain.  This var is simply to make testing less cumbersome.
# tupBlocksAndTx = GetChainFromGenTo(BlockCount)
# for CurrBlock in tupBlocksAndTx:
#     print("Block # " + str(CurrBlock.BlockNum) + " (Block Hash: " + CurrBlock.Hash + ")")
#     print("Transaction List:")
#     for currTx in CurrBlock.TXs:
#         print("- " + currTx.Hash)
#         jsnTxInfo = GetTxInfo(currTx.Hash)
#         if jsnTxInfo is not None:
#             print("Tx Info Type: " + str(type(jsnTxInfo)))
#             print("Vin Type: " + str(type(jsnTxInfo["vin"])))
#             if not IsMintTx(jsnTxInfo["vin"]):
#                 print("Unminted TX in block #" + str(CurrBlock.BlockNum))



print(GetHelpText("getrawmempool"))
#Turn on other miners
print("Network Hashrate: " + str(SendCommand(strRpc1Addr, "getnetworkhashps")))
print("Network Difficulty: " + str(SendCommand(strRpc1Addr, "getblockcount")))
print("Block Count: " + str(SendCommand(strRpc1Addr, "getblockcount")))
print("Miner2 Balance: " + str(SendCommand(strMin2Addr, "getbalance")))
print("Miner2 Hashrate: " + str(SendCommand(strMin2Addr, "gethashespersec")))
print("RPC1 Hashrate: " + str(SendCommand(strRpc1Addr, "gethashespersec")))
print("RPC2 Hashrate: " + str(SendCommand(strRpc2Addr, "gethashespersec")))
print("Miner2 Mempool: " + str(SendCommand(strMin2Addr, "getrawmempool")))
print("RPC1 Mempool: " + str(SendCommand(strRpc1Addr, "getrawmempool")))
print("RPC2 Mempool: " + str(SendCommand(strRpc2Addr, "getrawmempool")))


# print(SendCommand(strMin2Addr, "sendtoaddress", ("TWXQzj1rJtPzToZEvJYw7oXxqo1pQASMkw", 420.69,)))
# print(SendCommand(strRpc1Addr, "setgenerate", (True, -1,)))
# print(SendCommand(strRpc2Addr, "setgenerate", (True, -1,)))
# print(SendCommand(strMin2Addr, "setgenerate", (True, -1,)))

# print(SendCommand(strRpc1Addr, "setgenerate", (False,)))
# print(SendCommand(strRpc2Addr, "setgenerate", (False,)))
# print(SendCommand(strMin2Addr, "setgenerate", (False,)))

