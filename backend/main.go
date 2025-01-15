package main

import (
	"encoding/json"
	"net/http"
)

type ShortenUrlResponse struct {
	ShortenedUrl string
	Status       string
}

func handler(w http.ResponseWriter, r *http.Request) {
	// Создаем ответ
	response := ShortenUrlResponse{
		ShortenedUrl: "lol.com",
		Status:       "Success",
	}

	// Устанавливаем заголовок Content-Type
	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/api", handler)
	http.Handle("/", http.StripPrefix("/", http.FileServer(http.Dir("frontend/"))))
	http.ListenAndServe(":7783", nil)
}
