from jsonrpcclient import request, parse, Ok
import logging
import requests
#Program description
#This program exists to monitor the attacker and its transactions.  This program needs to query the blockchain and each transaction for each address.

#Variables
intCurrBlock = 0
strRpcAddr = 'http://<RPC Username Here>:<RPC Password Here>@<RPC IP Here>:<RPC Port Here>/'

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
    return SendCommand("help", (strCommand,))
    
def SendCommand(strCommand, pParams = ()):
    response = requests.post(strRpcAddr, json=request(strCommand, params = pParams)) 
    return ParseResponse(response)

#Get chain info from genesis to specified block number
def GetChainFromGenTo(intBlockNum):
    tupBlockchainInfo = ()
    for intCounter in range(intBlockNum + 1):  
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

#Main body
#First, get the block count
BlockCount = GetBlockCount()
print("Curr Block Count: " + str(BlockCount))
CurrBlockHash = GetSpecifiedBlockHash(BlockCount)
print("Curr Block Hash: " + str(CurrBlockHash))

#We really want the entire chain.  This var is simply to make testing less cumbersome.
tupBlocksAndTx = GetChainFromGenTo(100)
for currBlock in tupBlocksAndTx:
    print("Block # " + str(currBlock.BlockNum) + " (Block Hash: " + currBlock.Hash + ")")
    print("Transaction List:")
    for currTx in currBlock.TXs:
        print("- " + currTx.Hash)
        print(GetTxInfo(currTx.Hash))


print(GetHelpText("getrawtransaction"))