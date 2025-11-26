package middleware

import (
    "bytes"
    "io"
    "io/ioutil"
    "log"
    "net/http"
)

// LogRequestBody logs the incoming request body
func LogRequestBody(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Read the body
        bodyBytes, err := ioutil.ReadAll(r.Body)
        if err != nil {
            log.Println("Error reading body:", err)
            http.Error(w, "Can't read body", http.StatusInternalServerError)
            return
        }

        // Log it
        log.Println("Request Body:", string(bodyBytes))

        // Restore the io.ReadCloser to its original state
        r.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

        // Call the next handler
        next.ServeHTTP(w, r)
    })
}
