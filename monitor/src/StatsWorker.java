import mjson.Json;
import org.knowm.xchart.XYChart;

import javax.swing.*;
import java.util.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.stream.Collectors;

class StatsWorker extends SwingWorker<Boolean, Map<String, Boolean>> {

	// Charts
	JFrame frame;
	Map<String, XYChart> charts;
	// lock for syncing between worker thread and UI updating thread
	private Lock lock = new ReentrantLock();
	// variable names
	private List<String> vars;
	// map of pairs of lists of data (Y axis data)
	Map<String, LinkedList<Double>> varData = new HashMap<>();
	Map<String, Boolean> updatedVar = new HashMap<>();
	Map<String, String> varGroup = new HashMap<>();
	Map<String, List<String>> groupVars = new HashMap<>();
	// timestamp list of when packet was received (X axis)
	private LinkedList<Double> timestampData = new LinkedList<>();

	public StatsWorker(JFrame frame, Map<String, XYChart> charts, Json conf) {
		// Reading socket conf
		listener = new MulticastSocketListener(conf);
		// Flat mapping groups to list of strings
		vars = conf.at("VAR_GROUP")
			.asJsonMap()
			.values()
			.stream()
			.map(Json::asJsonList)
			.flatMap(List::stream)
			.map(Json::asString)
			.collect(Collectors.toList());
		// creating dataList for every variable
		vars.forEach(
			var -> {
				updatedVar.put(var, false);
				LinkedList<Double> dataList = new LinkedList<>();
				dataList.add(.0);
				varData.put(var, dataList);
			}
		);
		// Just for convenience...
		conf.at("VAR_GROUP")
			.asJsonMap()
			.forEach((k, v) -> {
				// both ways
				// var -> group
				v.asJsonList().forEach(var ->
					varGroup.put(var.asString(), k)
				);
				// group -> [vars...]
				groupVars.put(
					k,
					v.asJsonList()
						.stream()
						.map(Json::asString)
						.collect(Collectors.toList())
				);
		});
		// should not be empty...
		timestampData.add(.0);
		this.charts = charts;
		this.frame = frame;
	}

	private long startTime;
	private MulticastSocketListener listener;

	@Override
	protected Boolean doInBackground() throws Exception {
		startTime = System.currentTimeMillis();
		while (!isCancelled()) {
			// Read socket data once
			//System.out.println("Listening...");
			Json j = listener.listenOnce();
			//Mark time at which data was received to plot it
			long currentTime = System.currentTimeMillis();
			// Reseting booleans...
			// Setting lock because lists might not be the same size
			lock.lock();
			updatedVar.keySet().forEach((k) -> {
				updatedVar.put(k, false);
			});
			// Updating Y axes data...
			j.asJsonMap().forEach((k, v) -> {
				if(varData.containsKey(k)) {
					updateDataArray(varData.get(k), v.asDouble());
					updatedVar.put(k, true);
				}
			});
			// If value was not read, set to last value that was read... a.k.a. graph will be straight line...
			updatedVar.forEach((k, v) -> {
				if (!v) {
					updateDataArray(varData.get(k), varData.get(k).getLast());
					updatedVar.put(k, true);
				}
			});
			// Updating timestamp list...
			updateDataArray(timestampData, (currentTime - startTime) / 1000.);
			lock.unlock();
			// Tell GUI to update
			publish(updatedVar);
		}
		return true;
	}

	// convenience func
	private void updateDataArray(LinkedList<Double> data, double newPoint) {
		data.add(newPoint);
		if (data.size() > 50) {
			data.removeFirst();
		}
	}

	@Override
	protected void process(List<Map<String, Boolean>> chunks) {
		long t1 = System.currentTimeMillis();
		lock.lock();
		vars.forEach(v -> {
			charts
				.get(varGroup.get(v))
				.updateXYSeries(v, timestampData, varData.get(v), null);
		});
		lock.unlock();
		frame.revalidate();
		frame.repaint();
		long t2 = System.currentTimeMillis();
		try {
			if (40 - t2 + t1 > 0)
				Thread.sleep(40 - t2 + t1); // 40 ms ==> 25fps
			// Thread.sleep(400 - duration); // 40 ms ==> 2.5fps
		} catch (InterruptedException ignored) { }
	}
}