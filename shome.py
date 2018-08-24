from flask import Flask
from flask import request
import database as db
import telegram as tg
import json
import thread
import time
import sys


#=====================TELEGRAM SERVICE==================

def cmd_exec(mobile_id,mode,name,key,val):
	if key is None:
		return -1
	if mode == "GET":
		data = db.getSingleValue(key)
		#print data
		msgStr = "Status " + name+"("+key+ ")" + " = " + str(data[key])
		tg.sendMsg(mobile_id,msgStr)
	elif mode == "SET":
		param = {key:str(val)}
		db.updateField(param)
	if mode == "GETALL":
		data = db.getValue()
		#print data
		msgStr = 'Status : \r\n'
		for k, v in data.items():
			msgStr = msgStr + k + " = " + str(v) + '\r\n'
		tg.sendMsg(mobile_id,msgStr)
			

def telegram_pooling( threadName, delay):
	#print "%s: %s" % ( threadName, time.ctime(time.time()) )
	while True:
		msg = tg.getUpdate()
		if tg.waitNewMsg(msg) > 0:
			print ("Ada Pesan")
			#print tg.msgProcessing(msg)
			#print len(msg)
			mobile_id,(mode,name,key,val) = tg.msgProcessing(msg)
			cmd_exec(mobile_id,mode,name,key,val)
		time.sleep(delay)

#========================WEB SERVICE====================
app = Flask(__name__)
app.logger.disabled = True
def simpleSync(parameter):
	db.updateField(parameter)
	return db.getValue()

def methodExec(req, whois):
	mtd = req.args['method']
	param = req.args.copy()
	del param['user']
	del param['psw']
	del param['method']

	if mtd == 'test' :
		return 1,param
	elif mtd == 'simpleSync':
		return 1,simpleSync(param)
	else:
		return -1,param

def incomingPOST(req = None):
	if req is None:
		return 'Request Error !'
	return 'halo2'

def incomingGET(req = None):
	if req is None:
		return 'Request Error !'
	if 'method' not in req.args :
		return 'Parameter Error !'
	if 'user' not in req.args :
		return 'User Error !'
	if 'psw' not in req.args :
		return 'Password Error !'

	jobj = {}
	whois = db.auth(req.args['user'],req.args['psw'])
	if not whois:
		jobj['status'] = -1
		return json.dumps(jobj)
	jobj['status'],jobj['data'] = methodExec(req,whois)
	return json.dumps(jobj)

@app.route('/',methods=['GET', 'POST'])
def iot():
	ret = ''
	if request.method == 'POST':
		ret = incomingPOST(request)
	else :
		ret = incomingGET(request)

	if ret is None:
		jobj = {}
		jobj['status'] = -1
		ret = json.dumps(jobj)
		#print ret
	return ret

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return

if __name__ == '__main__':
	try:
		thread.start_new_thread( telegram_pooling, ("Thread-Telegram", 5, ) )
	except:
		print "Error: unable to start thread"
	app.run(host='0.0.0.0',port=6001,debug=True)
