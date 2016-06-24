#!/usr/bin/env python

import socket
import time
import sys
from datetime import datetime

from proto.packet_pb2     import Packet
from proto.publish_pb2    import Publish
from proto.request_pb2    import Request
from proto.response_pb2   import Response
from proto.pose_pb2       import Pose
from proto.subscribe_pb2  import Subscribe

MASTER_TCP_IP   = '127.0.0.1'
MASTER_TCP_PORT = 11345

NODE_TCP_IP     = '127.0.0.1'
NODE_TCP_PORT   = 11451

TCP_BUFFER_SIZE = 40960


# Listen for Subscribers
s_sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sub.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_sub.bind((NODE_TCP_IP, NODE_TCP_PORT))
s_sub.listen(5)


# Register as a Publisher with Gazebo
pk            = Packet()
pk.stamp.sec  = int(time.time())
pk.stamp.nsec = datetime.now().microsecond
pk.type       = "advertise"

pub           = Publish()
pub.topic     = "/gazebo/default/Pioneer3AT/cmd_vel"
pub.msg_type  = Pose.DESCRIPTOR.full_name
pub.host      = NODE_TCP_IP
pub.port      = NODE_TCP_PORT

whiteIpList = ['192.128.1.1', '192.128.1.2', '192.128.1.3', '192.128.1.4']

pk.serialized_data = pub.SerializeToString()

s_reg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_reg.connect((MASTER_TCP_IP, MASTER_TCP_PORT))
s_reg.send(hex(pk.ByteSize()).rjust(8))
s_reg.send(pk.SerializeToString())


# Respond to a subscriber
try:
  conn, address = s_sub.accept()
  data = conn.recv(TCP_BUFFER_SIZE)
  
  #Checking if the ip is allowed
  if (address in whiteIpList)
    # Decode Incomming Packet
    pk_sub = Packet()
    pk_sub.ParseFromString(data[8:])
    print "Packet:\n", pk_sub

    # Decode Subscription Request
    sub = Subscribe()
    sub.ParseFromString(pk_sub.serialized_data)
    print "Sub:\n", sub

    # Pack Data for Reply
    cmd_vel = Pose()
    cmd_vel.name = "Pioneer3AT"
    cmd_vel.position.x = 0.1
    cmd_vel.position.y = 0.2
    cmd_vel.position.z = 0.3
    cmd_vel.orientation.x = 1
    cmd_vel.orientation.y = 2
    cmd_vel.orientation.z = 3
    cmd_vel.orientation.w = 4

    # Publish Packet to Subscriber
    while 1:
      pk_pub            = Packet()
      pk_pub.stamp.sec  = int(time.time())
      pk_pub.stamp.nsec = datetime.now().microsecond
      pk_pub.type       = Pose.DESCRIPTOR.full_name
      pk_pub.serialized_data = cmd_vel.SerializeToString()

      conn.send(hex(cmd_vel.ByteSize()).rjust(8))
      conn.send(cmd_vel.SerializeToString())

      time.sleep(0.2)

finally:
  #This connection must remain open
  s_reg.close()
