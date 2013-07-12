ZMQ Latency test
================

This small python module runs a latency test with the passed number of 
packets


Usage
=====
Startup pong.py on the box that should bind a socket (no parameters)

Dependencies: txzmq, twisted, python 2.7


Startup ping.py on the box that should connect to a socket

Dependencies: txzmq, twisted, python 2.7

Command line arguments:

Positional argument (mandatory): the socket to connect to: for example: tcp://10.10.10.10:5555

--burstTime: the amount of packets to wait before sending a number of packets

--burstAmount: The amount of packets to send after each waiting period


Example: ping.py tcp://127.0.0.1:5555 --burstTime 0.01 --burstAmount 1000

This will burst a thousand packets every .01 seconds
