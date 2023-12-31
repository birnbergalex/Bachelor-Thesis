#!/usr/bin/env python3
import time
import socket
import struct
import random
import argparse

FILECACHE_CMD_READ  = 0
FILECACHE_CMD_LOAD  = 1
KEY                 = 0xb737fb1a
POS                 = 0
SIZE                = 1024
PORT                = 6666
RAND                = 0xdeadbeef

def main(args):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # Load file contents in memory
  message = struct.pack('<HIQII', FILECACHE_CMD_LOAD, KEY, POS, SIZE, RAND)
  s.sendto(message, (args.ip, PORT))
  s.recvfrom(4)

  # Read file contents
  message = struct.pack('<HIQIII', FILECACHE_CMD_READ, KEY, POS, SIZE, RAND, 0)
  start = time.perf_counter_ns()
  s.sendto(message, (args.ip, PORT))
  s.recvfrom(4)
  print(str((time.perf_counter_ns() - start) / 1_000_000) + ' ms')
  s.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Perform latency test")
  parser.add_argument("ip", help="The target IP address to perform the test on")
  args = parser.parse_args()
  main(args)
