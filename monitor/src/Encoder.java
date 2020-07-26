package encoders;

import mjson.Json;

import java.net.ProtocolException;

public interface Encoder {
	byte[] pack(Json js);
	Json unpack(byte[] buffer) throws ProtocolException;
	int getBufferSize();
}
