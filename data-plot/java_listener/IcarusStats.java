import mjson.Json;
import org.knowm.xchart.XChartPanel;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.XYChartBuilder;
import org.knowm.xchart.style.markers.None;

import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.List;
import java.util.*;

/**
 * Creates a real-time chart using SwingWorker
 */
public class IcarusStats {

  JFrame jf = new JFrame();
  MulticastSocketListener socketListener = new MulticastSocketListener("224.0.0.1", "192.168.1.101", 12000, 1024);
  Map<String, XYChart> charts = new HashMap<>();

  // variables to monitor
  private static String[] variables;

  public static void main(String[] args) {
    variables = args;
    Arrays.stream(args).forEach(System.out::println);
    IcarusStats swingWorkerRealTime = new IcarusStats();
    swingWorkerRealTime.go();
  }

  private void go() {

    JPanel jp = new JPanel(new GridBagLayout());
    GridBagConstraints cons = new GridBagConstraints();
    cons.fill = GridBagConstraints.HORIZONTAL;
    cons.weightx = 1;
    cons.gridx = 0;

    for (int i = 0; i < variables.length; i++ ) {
      // Create Chart
//      chart = QuickChart.getChart(variables[i], "Time", variables[i], variables[i], new double[] { 0 }, new double[] { 0 });
      XYChart chart = new XYChartBuilder().height(200).build();
      chart.addSeries(variables[i], new double[] { 0 }, new double[] { 0 });
//      chart.getStyler().setLegendVisible(false);
//      chart.getStyler().setXAxisTicksVisible(false);
//      chart.getStyler();
      chart.getSeriesMap().forEach((n,s) -> {s.setSmooth(true); s.setMarker(new None()); s.setLineColor(getRandomColor());});
      charts.put(variables[i], chart);
      // Show it
//    sw = new SwingWrapper<XYChart>(chart);
//    sw.displayChart();

      XChartPanel<XYChart> chartPanel = new XChartPanel<>(chart);
//      chartPanel.setSize(100, 30);

      //jp.add(new XChartPanel<>(QuickChart.getChart("SwingWorker XChart Real-time Demo", "Time", "Value", "randomData", new double[] { 0 }, new double[] { 0 })), cons);
      jp.add(chartPanel, cons);
    }
    jf.add(jp);
    jf.pack();
    jf.setLocationRelativeTo(null);
    MySwingWorker mySwingWorker = new MySwingWorker();
    mySwingWorker.execute();
    jf.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) {
        mySwingWorker.cancel(true);
      }
    });
    jf.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    jf.setVisible(true);
  }

  private Color getRandomColor(){
    Random rand = new Random();
    float r = rand.nextFloat() / 2f;
    float g = rand.nextFloat() / 2f;
    float b = rand.nextFloat() / 2f;
    // Will produce a random colour with more red in it (usually "pink-ish")
    return new Color(r, g, b);
  }

  private class MySwingWorker extends SwingWorker<Boolean, Map<String, LinkedList<Double>>> {

    long initialTime;
    LinkedList<Double> timestampList = new LinkedList<>();

    // map of pairs of lists of data
    Map<String, LinkedList<Double>> variableData = Collections.synchronizedMap(new HashMap<>());

    public MySwingWorker() {
      Arrays.stream(variables).forEach(
        var -> {
          LinkedList<Double> dataList = new LinkedList<>();
          dataList.add(.0);
          variableData.put(var,dataList);
        });
      timestampList.add(.0);
    }

    @Override
    protected Boolean doInBackground() throws Exception {
      initialTime = System.currentTimeMillis();
      while (!isCancelled()) {
        // Read socket data once
        Json j = socketListener.listenOnce();
        System.out.println(j.toString());
        //Mark time at which data was received to plot it
        long tmpTime = System.currentTimeMillis();

        variableData.forEach((k,v) -> {
          if( j.has(k)) {
            v.add(j.at(k).asDouble());
            if (v.size() > 50 /* || (tmpTime - initialTime) * 1000 - timestampList.getFirst() > 10 */) {
              v.removeFirst();
            }
          }
        });

        timestampList.add(((double)(tmpTime - initialTime))/1000);

        if (timestampList.size() > 50 /* || (tmpTime - initialTime) * 1000 - timestampList.getFirst() > 10 */) {
          timestampList.removeFirst();
        }

//        double[][] XYdata = new double[2][];
//        double[] Xdata = new double[timestampList.size()];
//        for (int i = 0; i < timestampList.size(); i++) {
//          Xdata[i] = timestampList.get(i);
//        }
//        double[] Ydata = new double[dataList.size()];
//        for (int i = 0; i < dataList.size(); i++) {
//          Ydata[i] = dataList.get(i);
//        }
//        XYdata[0] = Xdata;
//        XYdata[1] = Ydata;
//        publish(XYdata);
        publish(variableData);

        try {
          Thread.sleep(100);
        } catch (InterruptedException e) {
          System.out.println("Done.");
        }

      }

      return true;
    }

    @Override
    protected void process(List<Map<String, LinkedList<Double>>> chunks) {

      chunks.get(chunks.size() - 1).forEach((k,v) -> {
        charts.get(k).updateXYSeries(k, timestampList, v, null);
        jf.revalidate();
        jf.repaint();
      });


//      chart.updateXYSeries("randomData", mostRecentTimestamps, mostRecentDataSet, null);
//      jf.revalidate();
//      jf.repaint();

      long start = System.currentTimeMillis();
      long duration = System.currentTimeMillis() - start;
      try {
        Thread.sleep(40 - duration); // 40 ms ==> 25fps
        // Thread.sleep(400 - duration); // 40 ms ==> 2.5fps
      } catch (InterruptedException e) {
      }

    }
  }
}