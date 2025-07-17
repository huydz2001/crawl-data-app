package app.kafkastreams.app;

import java.util.List;
import java.util.Properties;

import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.Topology;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import app.kafkastreams.config.StreamsConfigHelper;
import app.kafkastreams.topology.CrawlDataTopology;

public class CrawlDataApp {
    private static final Logger logger = LoggerFactory.getLogger(CrawlDataApp.class);

    public static void main(String[] args) {
        Properties props = StreamsConfigHelper.getDefaultConfig("crawl-app", "kafka:9092");

        StreamsConfigHelper.createTopic(props, List.of(CrawlDataTopology.SOURCE_TOPIC, CrawlDataTopology.SINK_TOPIC));

        Topology topology = CrawlDataTopology.buildTopology();

        KafkaStreams streams = new KafkaStreams(topology, props);
        streams.start();
        System.out.println(topology.describe());

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutting down Kafka Streams application...");
            streams.close();
        }));
    }
}