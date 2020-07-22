import mjson.Json;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.util.Arrays;

public class MulticastSocketListener {

  String MCAST_ADDR = "224.0.0.1";
  String IF_ADDR = "192.168.1.101";
  int PORT = 12000;
  byte[] buffer;
  MulticastSocket clientSocket;

  public MulticastSocketListener(String multicastAddr, String interfaceIP, int port, int buffSize) {
    MCAST_ADDR = multicastAddr;
    IF_ADDR = interfaceIP;
    buffer = new byte[buffSize];
    try {
      // INIT SOCKET
      InetAddress mcastAddress = InetAddress.getByName(MCAST_ADDR);
      InetAddress ifAddress = InetAddress.getByName(IF_ADDR);
      clientSocket = new MulticastSocket(PORT);
      //Joint the Multicast group.
      clientSocket.setInterface(ifAddress);
      clientSocket.joinGroup(mcastAddress);

    } catch (IOException e) {
      e.printStackTrace();
    }
    PORT = port;

  }

  public Json listenOnce() throws IOException {
    // Get the address that we are going to connect to.

    // Create a buffer of bytes, which will be used to store
    // the incoming bytes containing the information from the server.
    // Since the message is small here, 256 bytes should be enough.
    Arrays.fill(buffer, (byte) 0);

    // Create a new Multicast socket (that will allow other sockets/programs
    // to join it as well.

    DatagramPacket msgPacket = new DatagramPacket(buffer, buffer.length);
    clientSocket.receive(msgPacket);
    String msg = new String(buffer, 0, buffer.length);
    return Json.read(msg);
  }
}