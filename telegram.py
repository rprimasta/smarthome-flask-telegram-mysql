#Thread for  TelegramBot
#Author : xxxx
#import library
import datetime
import time
import requests
import urllib
from parse import *

text_welcome = "Permintaan anda berhasil diproses.\r\nTerima Kasih."
#IGNORING LOW/UPPERCASE
text_var = [
	{'msg':'LAMP1', 'var':'btn0', 'rw':1},
	{'msg':'LAMP2', 'var':'btn1', 'rw':1},
	{'msg':'LAMP3', 'var':'btn2', 'rw':1},
	{'msg':'LAMP4', 'var':'btn3', 'rw':1},
	{'msg':'LAMP5', 'var':'btn4', 'rw':1},
	{'msg':'LAMP6', 'var':'btn5', 'rw':1},
	{'msg':'LAMP6', 'var':'btn6', 'rw':1},
	{'msg':'LAMP6', 'var':'btn7', 'rw':1},
	{'msg':'LAMP6', 'var':'btn8', 'rw':1},
	{'msg':'LAMP6', 'var':'btn9', 'rw':1},
	{'msg':'SENSOR0', 'var':'analog0', 'rw':0},
	{'msg':'SENSOR1', 'var':'analog1', 'rw':0},
	{'msg':'SENSOR2', 'var':'analog2', 'rw':0},
	{'msg':'SENSOR3', 'var':'analog3', 'rw':0}
]

text_val = [
	{'msg':'ON', 'val':1},
	{'msg':'OFF', 'val':0}
]

text_cmd = [
	{'cmd':'GET', 'mode':0},
	{'cmd':'SET', 'mode':1},
	{'cmd':'GETALL', 'mode':2}
]

cmd_format = "{cmd} {arg}"
cmdNoArg_format = "{cmd}"
get_format = "{msg}"
set_format = "{msg} {val}"


token = '551811703:AAGGnNaU8zrCf5LyYTokzJorWFAXpXToosg'
api_url = "https://api.telegram.org/bot{}/".format(token)
newOffset = {}

def sendMsg(chatId, txt):
	params = {'chat_id': chatId, 'text': txt, 'parse_mode': 'HTML'}
        method = 'sendMessage'
	global api_url
       	send = requests.post(api_url + method, params)
       	return send

def available (offset = 0, timeout = 10):
	method = 'getUpdates'
       	params = {'timeout': timeout, 'offset': offset}
       	global api_url
	url = api_url + method +'?'+  urllib.urlencode(params)
 	response = requests.get(url)
	#print url
	if response.status_code != 200:
		return None
	numMsg = response.json()['result']
    	return numMsg

def getChatId(dict):
	clist = []
	for item in dict:
		itm = item['message']['from']['id']
		if itm not in clist:
 			clist.append(itm)
	print clist
	return clist

def getNewestById(cid, dict):
	lastUpdate = 0;
	lastMsg = None
	#print "Search id " + str(cid)
	for item in dict:
		if cid == item['message']['chat']['id']:
			if item['message']['message_id'] > lastUpdate:
				lastUpdate = item['message']['message_id']
				lastMsg = item
	return lastMsg

def getUpdate(): 
	global newOffset
	res = available(offset=newOffset)
	#print res
	if res == None:
		return None

	id = getChatId(res)
	print len(id)

	resMsg = []
	for item in id:
		msgList = getNewestById(item,res)
		global newOffset
		if newOffset.has_key(str(item)) is True:
			#print msgList['message']['text']
			global newOffset
			#print str(msgList['message']['message_id']) +"|||"+str( newOffset[str(item)])
			if msgList['message']['message_id'] >= newOffset[str(item)]:
				print "New Message ...."
				resMsg.append(msgList['message'])

		global newOffset
		newOffset[str(item)] = msgList['message']['message_id'] + 1
		print newOffset
	#print resMsg
	return resMsg


def setCmd(arg=''):
	prs = parse(set_format, arg)
	for var in text_var:
		if prs['msg'].lower() == var['msg'].lower():
			for state in text_val:
				if prs['val'].lower() == state['msg'].lower():
					return "SET",prs['msg'],var['var'],state['val']
	return None

def getCmd(arg=''):
	prs = parse(get_format, arg)
	for var in text_var:
		if prs['msg'].lower() == var['msg'].lower():
			return "GET",prs['msg'],var['var'],1
	return None


def msgProcessing(msg):
	for ms in msg:
		prs = parse(cmd_format, ms['text'])
		if prs is None:
			prs = parse(cmdNoArg_format, ms['text'])
			if prs is None:
				return None,(None,None,None,-1)
		for cmd in text_cmd:
			if prs['cmd'].lower() == cmd['cmd'].lower():
				if cmd['mode'] == 0:
					action = getCmd(prs['arg'])
					if action is None:
						return None,(None,None,None,-1)
					global text_welcome
					msgStr = text_welcome
					sendMsg(ms['chat']['id'],msgStr)
					return ms['chat']['id'],action
				elif cmd['mode'] == 1:
					action = setCmd(prs['arg'])
					if action is None:
						return None,(None,None,None,-1)
					global text_welcome
					msgStr = text_welcome
					sendMsg(ms['chat']['id'],msgStr)
					return ms['chat']['id'],action
				elif cmd['mode'] == 2:
					global text_welcome
					msgStr = text_welcome
					sendMsg(ms['chat']['id'],msgStr)
					return ms['chat']['id'],('GETALL','ALL','ALL',0)
		return None,(None,None,None,-1)


def waitNewMsg(msg=[]):
	if not msg:
		return 0
	return len(msg)

#============TESTING AREA============
#while True:
#	msg = getUpdate()
#	if msg is not None:
		
#	if waitNewMsg(msg) > 0:
#		print msgProcessing(msg)
#	time.sleep(5)
