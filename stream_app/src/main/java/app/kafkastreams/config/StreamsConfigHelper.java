package app.kafkastreams.config;

import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.streams.StreamsConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Properties;
import java.util.stream.Collectors;

public class StreamsConfigHelper {
    private static final Logger logger = LoggerFactory.getLogger(StreamsConfigHelper.class);

    public static Properties getDefaultConfig(String appId, String bootstrapServers) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, appId);
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.Serdes$StringSerde");
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.Serdes$StringSerde");
        return props;
    }

    public static void createTopic(Properties config, List<String> topics) {
        try {
            AdminClient adminClient = AdminClient.create(config);
            var parttions = 2;
            short replicationFactor = 1;

            var newTopics = topics
                    .stream()
                    .map(topic -> new NewTopic(topic, parttions, replicationFactor))
                    .collect(Collectors.toList());

            var createTopicResult = adminClient.createTopics(newTopics);
            createTopicResult.all().get();
            logger.info("Topics created successfully");
        } catch (Exception e) {
            logger.error("Error creating topic", e);
        }
    }
}