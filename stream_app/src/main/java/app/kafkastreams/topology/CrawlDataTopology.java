package app.kafkastreams.topology;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CrawlDataTopology {
    private static final Logger logger = LoggerFactory.getLogger(CrawlDataTopology.class);
    public static final String SOURCE_TOPIC = "crawl-data";
    public static final String SINK_TOPIC = "crawl-data-filtered";

    public static Topology buildTopology() {

        StreamsBuilder streamsBuilder = new StreamsBuilder();
        KStream<String, String> crawlDataStream = streamsBuilder.stream(
                SOURCE_TOPIC,
                Consumed.with(Serdes.String(), Serdes.String()));

        crawlDataStream.print(Printed.<String, String>toSysOut().withLabel("crawl-data-stream"));

        KStream<String, String> filteredCrawlDatasStream = crawlDataStream
                .filter((key, value) -> {
                    try {
                        JSONObject json = new JSONObject(value);
                        return json.has("type") && json.getString("type").equalsIgnoreCase("news");
                    } catch (Exception e) {
                        logger.error("Error processing message", e);
                        return false;
                    }
                });

        filteredCrawlDatasStream.print(Printed.<String, String>toSysOut().withLabel("filtered-crawl-data-stream"));

        filteredCrawlDatasStream.to(SINK_TOPIC);
        return streamsBuilder.build();
    }
}