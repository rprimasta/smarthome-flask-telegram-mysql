import mysql.connector
import dbconfig as dbConf

mydb = mysql.connector.connect(
  host=dbConf.host(),
  user=dbConf.user(),
  passwd=dbConf.passwd(),
  database=dbConf.database()
)

mycursor = mydb.cursor(dictionary=True,buffered=True)

def updateSingleField(field='',value=''):
	sql = "UPDATE `tbl_broker` SET `VALUE`='" +value+ "' WHERE FIELD = '" + field +"';" 
	mycursor.execute(sql)
	mydb.commit()
	return mycursor.rowcount
	#print sptr.join(values)


def updateField(parameter):
	rows = []
	for key, value in parameter.items():
		sql = "UPDATE `tbl_broker` SET `VALUE`='" +value+ "' WHERE FIELD = '" + key +"';" 
		mycursor.execute(sql)
	mydb.commit()
	return mycursor.rowcount
	#print sptr.join(values)


def auth(user, psw):
	sql = "SELECT * FROM tbl_user WHERE tbl_user.user = '"+user+"' AND password=PASSWORD('"+psw+"')"
	#print sql
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	return myresult

def getValue():
	sql = "SELECT * FROM tbl_broker"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	arrResult = {}
	for v in myresult:
		arrResult[v['FIELD']] = v['VALUE']
	return arrResult

def getSingleValue(field=''):
	sql = "SELECT * FROM tbl_broker WHERE tbl_broker.FIELD = '" + field + "'"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	arrResult = {}
	for v in myresult:
		arrResult[v['FIELD']] = v['VALUE']
	return arrResult

#getValue();
