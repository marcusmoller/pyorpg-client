import time, json

def log(msg):
	''' Prints @msg to the terminal with a timestamp '''
	localTime = time.localtime(time.time())
	stringTime = str(localTime[3]) + ":" + str(localTime[4]) + ":" + str(localTime[5])

	print stringTime + ": " + msg

def decodeJSON(data):
	'''Decodes JSON from a @data'''
	result = json.loads(data)
	
	return result