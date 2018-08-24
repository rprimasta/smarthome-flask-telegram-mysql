from flask import Flask
from flask import request
import database as db
import telegram as tg
import json
import thread
import time
import sys
from raven.contrib.flask import Sentry
#from threading import Thread

#kill all with 
#pkill --signal 9 -e -f shome.py
#import os
#os.system('pkill --signal 9 -e -f shome.py')


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
	print "Init Thread pooling"
	print "%s: %s" % ( threadName, time.ctime(time.time()) )
	while True:
		msg = tg.getUpdate()
		if tg.waitNewMsg(msg) > 0:
			print ("Ada Pesan")
			mobile_id,(mode,name,key,val) = tg.msgProcessing(msg)
			cmd_exec(mobile_id,mode,name,key,val)
		time.sleep(delay)

#========================WEB SERVICE====================
app = Flask(__name__)
app.logger.disabled = True
sentry = Sentry(app, dsn='https://ddf4d10c09ab417882af9c644e013f10:b739844829d94d58b71e800f2f3410cc@sentry.io/1267055')
sentry.init_app(app)


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
	try:
		if request.method == 'POST':
			ret = incomingPOST(request)
		else :
			ret = incomingGET(request)

		if ret is None:
			jobj = {}
			jobj['status'] = -1
			ret = json.dumps(jobj)
			#print ret
	except ZeroDivisionError:
    		sentry.captureException()
		jobj = {}
		jobj['status'] = -1
		ret = json.dumps(jobj)	
	return ret

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return

thread.start_new_thread(telegram_pooling,("Thread-Telegram",10, ))
sentry.captureMessage('Smart Home Started...')
app.run(host='0.0.0.0',port=6001,debug=False)

