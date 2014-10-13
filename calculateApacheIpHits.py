#!/usr/bin/python
#encoding:utf-8
try:
	import sys,optparse, datetime,re
except:
	print("Error running 'import sys,optparse,datetime,re'. Maybe you have to install some python library")
	
def isValid(ip):
	if (re.match("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",ip)):
		return True
	elif re.match(r'^[a-zA-Z0-9_]{,63}(\.[a-zA-Z0-9_]{,63}){3}$',ip): #("^\W+(\.\W)$", ip):
		return True
	else:
		#print "Name/IP host wrong. You have to write a FQDN name or a IP direction"
		return False
	return False
	
def readHistoryIP(logfile,sec, deltaday,deltahour,deltaminutes):
	months = {"Ene":1, "Feb":2, "Mar":3, "Abr":4, "May":5, "Jun":6, "Jul":7, "Ago":8, "Sept":9, "Oct":10, "Nov":11, "Dic":12}
	today = datetime.datetime.now()
	refDay= datetime.timedelta(days=int(deltaday), hours=int(deltahour), minutes=int(deltaminutes))
 
	ipHitListing = { }
	try:
		contents = open(logfile, "r")
	except IOError, e:
		print 'Error openning file '+ logfile +": "+e.strerror
		raise
	except:
		print 'Error openning file '+ logfile
		raise
	# go through each line of the logfile
	for line in contents:
		# split the string to isolate the IP address and date
		ip = line.split(" ", 1)[0]
		dateRecord=line.split(" ",5)[4][1:]
		date = dateRecord.split(":",1)[0]
		day=date.split("/",1)[0]
		month=date.split("/",2)[1]
		year =date.split("/",3)[2]
		hour = dateRecord.split(":",2)[1]
		minute = dateRecord.split(":",3)[2]
		seconds = dateRecord.split(":",4)[3]
		eventdate=datetime.datetime(int(year),int(months[month]),int(day),int(hour),int(minute),int(seconds))
		#Check if ip is right
		#print "Analizing IP: '" + ip + "'"
		if isValid(ip):
			if eventdate > today - refDay:
				intervalDelta=datetime.timedelta(seconds=int(sec))
				count=False
				if (ip in ipHitListing):		
					for ipData in ipHitListing[ip].items():
						if eventdate < ipData[0] + intervalDelta:
							ipHitListing[ip]= {ipData[0]:int(ipData[1])+1}
							count=True
							break
					if count == False:
						ipHitListing[ip]= {eventdate:1}
				else:
					ipHitListing[ip]= {eventdate:1}
	return ipHitListing
def main():
	parser = optparse.OptionParser("usage%prog " + "[-f <file>] -n Number of events -s seconds to find events -d number of days to analice -H number of hours to analice -m number of minutes to analice")
	parser.add_option('-f', dest = 'file', type = 'string', help = 'Please, specify the Apache access file', default="/var/log/apache2/access.log")
	parser.add_option('-n', dest = 'number', type = 'string', help = 'Please, specify the number of connections to detect. By default 10', default="10")
	parser.add_option('-d', dest = 'deltaday', type = 'string', help = 'Please, specify the number of days to check. By default 10', default="10")
	parser.add_option('-H', dest = 'deltahour', type = 'string', help = 'Please, specify the number of hours to check. By default 10', default="10")
	parser.add_option('-m', dest = 'deltaminute', type = 'string', help = 'Please, specify the number of minutes to check. By default 10', default="10")
	parser.add_option('-s', dest = 'seconds', type = 'string', help = 'Please, specify the seconds. By default: 1"', default="1")
	(options, args) = parser.parse_args()
	HitsDictionary = readHistoryIP(options.file,options.seconds, options.deltaday, options.deltahour, options.deltaminute)
	for ip in HitsDictionary.keys():
		if HitsDictionary[ip].values()[0] > int(options.number):
			print "Attention---> IP: " + ip + ", " + str(HitsDictionary[ip].values()[0]) + " access in " + options.seconds + " seconds"
if __name__ == "__main__":
	main()