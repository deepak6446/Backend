package kafka

import (
	"context"
	"log"

	"github.com/segmentio/kafka-go"
)

func SendMessageToKafka(message []byte) error {
	kafkaURL := "localhost:9092" // or your Kafka URL
	topic := "example-topic"

	writer := kafka.NewWriter(kafka.WriterConfig{
		Brokers:  []string{kafkaURL},
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	})

	msg := kafka.Message{
		Value: message,
	}

	if err := writer.WriteMessages(context.Background(), msg); err != nil {
		log.Printf("failed to write messages to kafka: %v", err)
		return err
	}
	log.Println("Message sent to Kafka: ", string(message))
	return writer.Close()
}
