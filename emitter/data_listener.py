import socket


# for pings in range(10):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     #client_socket.settimeout(1.0)
#     message = b'test'
#     addr = ("127.0.0.1", 12000)

#     start = time.time()
#     client_socket.sendto(message, addr)
#     try:
#         data, server = client_socket.recvfrom(1024)
#         end = time.time()
#         elapsed = end - start
#         print(f'{data} {pings} {elapsed}')
#     except socket.timeout:
#         print('REQUEST TIMED OUT')

import binascii

def main():
  MCAST_GRP = '224.1.1.1'
  MCAST_PORT = 12000
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  except AttributeError:
    pass
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

  sock.bind((MCAST_GRP, MCAST_PORT))
  print(socket.gethostname())
  #host = socket.gethostbyname(socket.gethostname())
  host = '192.168.1.101'
  sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
  sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
                   socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

  while 1:
    try:
      data, addr = sock.recvfrom(1024)
      print(data.decode('utf8'))
    except socket.error:
      print('Error')
      #print 'Expection'
      #hexdata = binascii.hexlify(data)
      #print 'Data = %s' % hexdata

if __name__ == '__main__':
  main()