/**
 * Thread for writing data to disk without slowing down actual graph...
 */
public class DataWriter implements Runnable {

	// TODO
	@Override
	public void run() {
		while(true) {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
