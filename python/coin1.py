#!/usr/bin/python

from socket import *
from select import select
import sys
import time


def get_coin_try() :
	global total_coin
	global total_try

	data = sock.recv(BUFSIZE)
	print ("<< recv: %s" % data)
	# <<recv: N=480 C=9

	coins = data.split('=')[1] #480 C

	trys = (data.split('=')[2]).split("\n")[0]
	coins = coins.split(' ')[0]

 
	total_coin = int(coins)
	total_try = int(trys)

	return


# check the half of coins
def check_range(start, end) : 
	print "check_range %d %d" %(start, end)

	result = ""
	for i in range(start, end + 1):
		result += str(i) + " "
	result += "\n"

	print (">> send: %s" % result)
	sock.send(result);

	weigh = sock.recv(BUFSIZE)
	print ("<< recv: %s" % weigh)
	if ((int(weigh)) % 10) != 0 :
		print ("- we have counterfeit in half")
		return 1
	else : 
		print ("- we do Not have counterfeit in half")
		return 0



# split left and right
def split_left_right(start, end, cnt) :

	global total_try

	print "enter split : %d ~ %d" %(start, end)

	#find answer
	if start >= end:
		print "we found %d" %start
		return start;

	cnt = cnt - 1
	print "count : %d / %d" %(cnt, total_try)
	if cnt == 0:
		print "count is 0"
		print "start/end : %d %d" % (start, end)




	left_start = start
	left_end = start + (end - start) / 2
	
	right_start = left_end + 1
	right_end = end

		

	check_have = check_range(left_start, left_end)
	if check_have == 1 :
		print "split left start/end : %d %d" % (left_start, left_end)
		final_result = split_left_right(left_start, left_end, cnt)	
	else :
		print "split right start/end : %d %d" % (right_start, right_end)
		final_result = split_left_right(right_start, right_end, cnt)

	return final_result


# start here ---------------------

# nc pwnable.kr 9007
HOST = 'pwnable.kr'
PORT = 9007 
BUFSIZE = 1024 * 10
ADDR = (HOST, PORT)

sock = socket(AF_INET, SOCK_STREAM)

try:
    sock.connect(ADDR)
except Exception as e:
    print('can not connect(%s:%s)' % ADDR)
    sys.exit()

print('connected with (%s:%s)' % ADDR)


data = sock.recv(BUFSIZE)
print ("<< recv: %s" % data) # this is for explanation


#------------------------

for i in range(0, 101) :
	get_coin_try()
	print "start with total coin: %d  total try: %d" % (total_coin, total_try)

	final_result = split_left_right(0, total_coin, total_try)

	print ">> final_send: %s" % final_result
	sock.send(str(final_result) + "\n");

	data = sock.recv(BUFSIZE)
	print "<< recv: %s" % data

	while data.find('Correct') == -1 :
		print (">> final_send: %s" % final_result)
		sock.send(str(final_result) + "\n");

		data = sock.recv(BUFSIZE)
		print ("<< recv: %s" % data)
	
	print "--------------------------------------------"


data = sock.recv(BUFSIZE)
print ("<< recv: %s" % data)

print "exit"
sock.close()
