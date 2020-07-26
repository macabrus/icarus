package encoders;

import mjson.Json;

import java.net.ProtocolException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.*;
import java.util.stream.Collectors;

public class BitEncoder implements Encoder {

	private int BUFFER_SIZE = 82;
	private final String RECEIVE_PATTERN = "hidddddddddf";
	private final ByteOrder ENDIANNESS = ByteOrder.LITTLE_ENDIAN;
	private final String SEND_PATTERN = "hidddddddddf";
	private final int ACC = 0x06;
	private final int GYR = 0x1e;
	private final int MAG = 0x36;
	private final int TMP = 0x4e;

	public BitEncoder() {
		varOrdered = varOffset.entrySet().stream().sorted((v1, v2) ->
			v1.getValue() > v2.getValue() ? 1 : -1
		).map(Map.Entry::getKey).collect(Collectors.toList());
	}

	public BitEncoder(int bufferSize) {
		this();
		this.BUFFER_SIZE = bufferSize;
	}

	public byte[] pack(Json js) {
		int  control = 1, mask = 0;
		ByteBuffer buffer = ByteBuffer.allocate(BUFFER_SIZE);
		buffer.order(ENDIANNESS);
		buffer.putShort((short) control);
		buffer.putInt(mask);
		int i = 0;
		for(Map.Entry<String, Character> e : varType) {
			System.out.println(e);
			Json var = js.at(e.getKey());
			if(var != null) {
				mask += 1 << (31 - i);
				byte[] packed = packValue(e.getValue(), var);
				print(packed);
				buffer.put(packed);
			}
			else {
				buffer.put(packValue(e.getValue(), Json.factory().number(0)));
			}
			i++;
		}
		buffer.putInt(0x02, mask);
		return buffer.array();
	}

	public Json unpack(byte[] data) throws ProtocolException {
		Json js = Json.object();
		ByteBuffer buffer = ByteBuffer.wrap(data);
		buffer.order(ENDIANNESS);
		short control = buffer.getShort();
		if (control != 1) {
			throw new ProtocolException(String.format("Protocol version %x not supported!", control));
		}
		int mask = buffer.getInt();
		System.out.println("MASK "+ mask);
		for (int i = 0; i != varOrdered.size() && i + 2 < RECEIVE_PATTERN.length(); i ++) {
			if ((mask & (1 << (31 - i))) > 0) {
				String var = varOrdered.get(i);
				int offset = varOffset.get(var);
				char type = RECEIVE_PATTERN.charAt(i+2);
				int len = typeSize.get(type);
				System.out.println(var);
				System.out.println(type);
				System.out.println(len);
				System.out.println(offset);
				byte[] dst = new byte[len];
				for ( int j = 0; j < len; j++) {
					dst[j] = buffer.get(offset++);
				}
				js.set(var, unpackValue(type, dst));
			}
		}
		return js;
	}

	private byte[] packValue(Character type, Json val) {
		ByteBuffer b = ByteBuffer.allocate(typeSize.get(type));
		b.order(ENDIANNESS);
		switch(type) {
			case 'd':
				b.putDouble(val.asDouble());
				break;
			case 'f':
				b.putFloat(val.asFloat());
				break;
			case 'i':
				b.putInt(val.asInteger());
				break;
		}
		return b.array();
	}

	private Object unpackValue(Character type, byte[] val) {
		ByteBuffer buffer = ByteBuffer.wrap(val);
		buffer.order(ENDIANNESS);
		switch(type) {
			case 'd':
				return buffer.getDouble();
			case 'f':
				return buffer.getFloat();
			case 'i':
				return buffer.getInt();
		}
		return null;
	}

	// Sizes of encoded data
	private Map<Character, Integer> typeSize = new HashMap<Character, Integer>(){{
			put('i', 4);
			put('d', 8);
			put('f', 4);
	}};

	// Type of each var
	private List<Map.Entry<String, Character>> varType = new ArrayList<Map.Entry<String, Character>>() {
		private void put(String k, Character v) {
			add(new AbstractMap.SimpleEntry<>(k, v));
		}
		{
			put("accX", 'd');
			put("accY", 'd');
			put("accZ", 'd');
			put("gyrX", 'd');
			put("gyrY", 'd');
			put("gyrZ", 'd');
			put("magX", 'd');
			put("magY", 'd');
			put("magZ", 'd');
			put("temp", 'f');
		}
	};

	// Address in buffer for each var
	private Map<String, Integer> varOffset = new HashMap<String, Integer>() {{
			put("accX",ACC + 0x00);
			put("accY",ACC + 0x08);
			put("accZ",ACC + 0x10);
			put("gyrX",GYR + 0x00);
			put("gyrY",GYR + 0x08);
			put("gyrZ",GYR + 0x10);
			put("magX",MAG + 0x00);
			put("magY",MAG + 0x08);
			put("magZ",MAG + 0x10);
			put("temp",TMP + 0x00);
	}};

	private List<String> varOrdered;

	private static void print(byte[] buffer) {
		System.out.print("[ ");
		for (byte b : buffer) System.out.print(String.format("0x%02X ", b));
		System.out.println("]");
	}

	public int getBufferSize() {
		return BUFFER_SIZE;
	}

}
