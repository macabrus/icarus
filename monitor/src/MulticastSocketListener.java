import mjson.Json;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.net.SocketTimeoutException;
import java.util.Arrays;

public class MulticastSocketListener {

  private String MCAST_IP;
  private String IF_IP;
  private int PORT;
  private byte[] BUFFER;
  private MulticastSocket clientSocket;

  public MulticastSocketListener(Json conf) throws IOException {
    MCAST_IP = conf.at("MCAST_IP").asString();
    IF_IP = conf.at("IF_IP").asString();
    BUFFER = new byte[conf.at("BUFF_SIZE").asInteger()];
    PORT = conf.at("PORT") == null ? conf.at("PORT").asInteger() : 12000;
    // Initialize socket
    InetAddress mcastAddress = InetAddress.getByName(MCAST_IP);
    InetAddress ifAddress = InetAddress.getByName(IF_IP);
    clientSocket = new MulticastSocket(PORT);
    //Joint the Multicast group.
    clientSocket.setInterface(ifAddress);
    clientSocket.joinGroup(mcastAddress);
    clientSocket.setSoTimeout((int) (conf.at("TIMEOUT") != null ? conf.at("TIMEOUT").asFloat() * 1000 : 500));
  }

  public Json listenOnce() throws IOException {
    Arrays.fill(BUFFER, (byte) 0);
    DatagramPacket msgPacket = new DatagramPacket(BUFFER, BUFFER.length);
    String msg;
    try {
      clientSocket.receive(msgPacket);
      msg = new String(BUFFER, 0, BUFFER.length);
    } catch (SocketTimeoutException e) {
//      e.printStackTrace();
      msg = "{}";
    }
    return Json.read(msg);
  }
}