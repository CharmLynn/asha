#! /usr/bin/en -python

import sys
import os
import datetimekey
import logging
import redis as rd
import MySQLdb

r=redis.Redis(host='localhost',port=6379,db=0)

dateyesterday= (datetime.datetime.now()-datetime.timedelta(days = 2)).strftime("%Y%m%d")
date2daysbf= (datetime.datetime.now()-datetime.timedelta(days = 3)).strftime("%Y%m%d")


filedir = "/home/asha/workbench"
dateyesterday = filedir+"/"+datetoday+".log"

if os.path.exists(dateyesterday):
	print "file exitis"
	logging.info("yesterday log file exits")
else:
	print "file is not exits"
	logging.warning("today log file is not exits")
	sys.exit(1)


key_histor = date2daysbf + 'history'
key_active = dateyesterday +'_active'
key_new = dateyesterday + '_new'
active_value = r.scard(key_active)
r.sdiffstore(key_new,key_active,key_history)
new_value = r.scard(key_new)


try:
	conn = MySQLdb.connect(host='localhost',user='asha',passwd='asha',port=3306,db='bi')
	cur.cursor()
	cur.execute('insert into day_result(dateday,uv,nv) values(%s,%s,%s)',(dateyesterday,active_value,new_value))

	for i in range(2,8):
		dateoffset = date2daysbf= (datetime.datetime.now()-datetime.timedelta(days = i)).strftime("%Y%m%d")
		j = i - 1
		remainvalue =  r.sinter(dateoffset+'_new', active_value)
		if i == 2:
			cur.execute('insert into day_result(dateday,j+'_remain') values(%s,%s)',(dateyesterday, remainvalue))
			r.sdiffstore(dateoffset+'_sleep',dateoffset+'_new',active_value)
		else:
			cur.execute('update day_result set j+"_remain" = remainvalue where dateday = dateoffset')
			r.sdiff(dateoffset+'_sleep',dateoffset+'_sleep',active_value)
		sleepvalue = r.scard(dateoffset+'_sleep')
		cur.execute('insert into day_result(dateday,sleepvalue,checkdate) values(%s,%s,%s)',(dateoffset,sleepvalue,dateyesterday))
	for i in range(9,31):
		dateoffset = date2daysbf= (datetime.datetime.now()-datetime.timedelta(days = i)).strftime("%Y%m%d")
		r.sdiff(dateoffset+'_sleep',dateoffset+'_sleep',active_value)
		sleepvalue = r.scard(dateoffset+'_sleep')
		cur.execute('insert into day_result(dateday,sleepvalue,checkdate) values(%s,%s,%s)',(dateoffset,sleepvalue,dateyesterday))

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

