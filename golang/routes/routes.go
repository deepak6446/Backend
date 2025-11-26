package routes

import (
	"golang/handlers"

	"github.com/gorilla/mux"
)

func RegisterRoutes(router *mux.Router) {
	router.HandleFunc("/post-message", handlers.PostMessageHandler).Methods("POST")
}
