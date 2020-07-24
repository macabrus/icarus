import mjson.Json;
import org.knowm.xchart.XChartPanel;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.XYChartBuilder;
import org.knowm.xchart.style.Styler;
import org.knowm.xchart.style.markers.None;

import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

/**
 * Creates a real-time chart using SwingWorker
 */
public class IcarusStats {

	JFrame jf = new JFrame();
	private static MulticastSocketListener socketListener;
	Map<String, XYChart> charts = new HashMap<>();
	private static Json conf;

	public static void main(String[] args) throws IOException {
		// Reading configs
		conf = Json.read(readFile(args[0], Charset.forName("UTF-8")));
		IcarusStats icarusStats = new IcarusStats();
		icarusStats.go();
	}

	private void go() throws IOException {
		JScrollPane sp = new JScrollPane();
		JPanel jp = new JPanel(new GridBagLayout());
		sp.setViewportView(jp);
		GridBagConstraints gbc = new GridBagConstraints();
		gbc.fill = GridBagConstraints.HORIZONTAL;
		gbc.weightx = 1;
		gbc.gridx = 0;
		conf.at("VAR_GROUP").asJsonMap().forEach((k, group) -> {
			String unit = conf.at("VAR_UNIT").at(k) != null ? conf.at("VAR_UNIT").at(k).asString() : null;
			XYChart chart = new XYChartBuilder()
				.title(
					(conf.at("VAR_LABEL").at(k) != null ?
					conf.at("VAR_LABEL").at(k).asString() : "") + String.format(" [%s]",unit))
				.theme(Styler.ChartTheme.Matlab)
				.height(conf.at("PLOT_HEIGHT") != null ? conf.at("PLOT_HEIGHT").asInteger() : 200)
				.build();
			group.asJsonList().forEach(var -> {
				chart.addSeries(
					var.asString(),
					new double[] { 0 },
					new double[] { 0 }
				);
			});
			chart.getSeriesMap().forEach((n,s) -> {
				s.setSmooth(true);
				s.setMarker(new None());
				String color = conf.at("VAR_COLOR").at(n) != null ? conf.at("VAR_COLOR").at(n).asString() : "#000";
				s.setLineColor(Color.decode(color));
				String label = conf.at("VAR_LABEL").at(n) != null ? conf.at("VAR_LABEL").at(n).asString() : null;
				s.setLabel(label);
			});
			chart.getStyler().setXAxisTitleVisible(true);
			chart.getStyler().setYAxisTitleVisible(true);
			charts.put(k, chart);
			XChartPanel<XYChart> chartPanel = new XChartPanel<>(chart);
			jp.add(chartPanel, gbc);
		});
		// Background worker for listening on socket
		// passing configuration to worker
		StatsWorker mySwingWorker = new StatsWorker(jf, charts, conf);
		mySwingWorker.execute();
		// Setting up JFrame
		jf.add(sp);
		jf.setSize(1000, 900);
		// Kill worker on close
		jf.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				mySwingWorker.cancel(true);
			}
		});
		// Kill AWT event thread on exit to quit appropriately
		jf.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		jf.setLocationRelativeTo(null);
		jf.setVisible(true);
	}

	static String readFile(String path, Charset encoding) throws IOException {
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return new String(encoded, encoding);
	}
}
