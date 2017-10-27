package http

import (
	"net/http"
	"testing"
	"github.com/julienschmidt/httprouter"
)


func TestR(t *testing.T) {
	r := httprouter.New()
	r.GET("/", func (w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
		w.Write([]byte("Index"))
	})

	t.Fatal(http.ListenAndServe(":8080", r))
}