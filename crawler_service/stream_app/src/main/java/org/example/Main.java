package org.example;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "filter-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> source = builder.stream("raw-data-topic",
                Consumed.with(Serdes.String(), Serdes.String()));

        KStream<String, String> filtered = source.filter((key, value) -> {
            try {
                logger.info("Processing key={}, value={}", key, value);
                JSONObject json = new JSONObject(value);
                return json.has("type") && json.getString("type").equalsIgnoreCase("news");
            } catch (Exception e) {
                logger.error("Error processing message", e);
                return false;
            }
        });

        filtered.to("filtered-data-topic", Produced.with(Serdes.String(), Serdes.String()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);

        // Thêm state listener để log trạng thái kết nối
        streams.setStateListener((newState, oldState) -> {
            logger.info("Kafka Streams state changed from {} to {}", oldState, newState);
            if (newState == KafkaStreams.State.RUNNING) {
                logger.info("Kafka Streams application CONNECTED and RUNNING!");
            }
            if (newState == KafkaStreams.State.ERROR) {
                logger.error("Kafka Streams application entered ERROR state!");
            }
        });
        streams.start();

        Topology topology = builder.build();
        System.out.println(topology.describe());

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutting down Kafka Streams application...");
            streams.close();
        }));

    }
}