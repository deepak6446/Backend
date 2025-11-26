package handlers

import (
	"golang/kafka"
	"io/ioutil"
	"log"
	"net/http"
)

func PostMessageHandler(w http.ResponseWriter, r *http.Request) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	log.Println("Received body: ", string(body))

	err = kafka.SendMessageToKafka(body)
	if err != nil {
		http.Error(w, "Failed to send message to Kafka", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Message sent to Kafka"))
}
