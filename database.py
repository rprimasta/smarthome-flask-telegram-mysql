import mysql.connector
import dbconfig as dbConf



def updateSingleField(field='',value=''):
	mydb = mysql.connector.connect(host=dbConf.host(),user=dbConf.user(),passwd=dbConf.passwd(),database=dbConf.database())
	mycursor = mydb.cursor(dictionary=True,buffered=True)
	sql = "UPDATE `tbl_broker` SET `VALUE`='" +value+ "' WHERE FIELD = '" + field +"';" 
	mycursor.execute(sql)
	mydb.commit()
	mydb.close()
	return mycursor.rowcount
	#print sptr.join(values)


def updateField(parameter):
	mydb = mysql.connector.connect(host=dbConf.host(),user=dbConf.user(),passwd=dbConf.passwd(),database=dbConf.database())
	mycursor = mydb.cursor(dictionary=True,buffered=True)
	rows = []
	for key, value in parameter.items():
		sql = "UPDATE `tbl_broker` SET `VALUE`='" +value+ "' WHERE FIELD = '" + key +"';" 
		mycursor.execute(sql)
	mydb.commit()
	mydb.close()
	return mycursor.rowcount
	#print sptr.join(values)


def auth(user, psw):
	mydb = mysql.connector.connect(host=dbConf.host(),user=dbConf.user(),passwd=dbConf.passwd(),database=dbConf.database())
	mycursor = mydb.cursor(dictionary=True,buffered=True)
	sql = "SELECT * FROM tbl_user WHERE tbl_user.user = '"+user+"' AND password=PASSWORD('"+psw+"')"
	#print sql
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	mydb.commit()
	mydb.close()
	return myresult

def getValue():
	mydb = mysql.connector.connect(host=dbConf.host(),user=dbConf.user(),passwd=dbConf.passwd(),database=dbConf.database())
	mycursor = mydb.cursor(dictionary=True,buffered=True)
	sql = "SELECT * FROM tbl_broker"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	arrResult = {}
	for v in myresult:
		arrResult[v['FIELD']] = v['VALUE']
	mydb.commit()
	mydb.close()
	return arrResult

def getSingleValue(field=''):
	mydb = mysql.connector.connect(host=dbConf.host(),user=dbConf.user(),passwd=dbConf.passwd(),database=dbConf.database())
	mycursor = mydb.cursor(dictionary=True,buffered=True)
	sql = "SELECT * FROM tbl_broker WHERE tbl_broker.FIELD = '" + field + "'"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	arrResult = {}
	for v in myresult:
		arrResult[v['FIELD']] = v['VALUE']
	return arrResult
	mydb.commit()
	mydb.close()

