package http

import (
	"testing"
	"net/http"
	"fmt"
	"io/ioutil"
	"time"
	"net"
)

const port  = ":8080"

func TestRun(t *testing.T) {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Hello World"))
	})

	err := http.ListenAndServe(port, nil)
	if err != nil {
		t.Fatalf("start http server fail: %v", err)
	}
}

func TestServeMux(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Hello World Mux"))
	})

	err := http.ListenAndServe(port, mux)
	if err != nil {
		t.Fatalf("start http server fail: %v", err)
	}
}


type Handler func(http.ResponseWriter, *http.Request)
func (f Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("---- ServeHTTP ----\n"))
	f(w, r)
}

func TestHandle(t *testing.T) {
	var handler Handler = func (w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("TestHandle"))
	}
	// Handle accept a interface rather than a function in HandleFunc
	http.Handle("/", handler)

	if err := http.ListenAndServe(port, nil); err != nil {
		t.Fatalf("start http server fail: %v", err)
	}
}


func TestHttpServer(t *testing.T) {
	var handler Handler = func (w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("TestHttpServer"))
	}

	// just what does http.ListenAndServe do
	server := &http.Server{
		Handler:      handler, // interface http.Handler ServeHTTP
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	ln, err := net.Listen("tcp", port)
	if err != nil {
		t.Fatal(err)
	}

	if err = server.Serve(ln); err != nil {
		t.Fatalf("start http server fail: %v", err)
	}
}


func TestClient(t *testing.T) {
	resp, err := http.Get(fmt.Sprintf("http://127.0.0.1%s", port ))
	if err != nil {
		t.Fatalf("client error: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("read body error: %v", err)
	}
	t.Log(string(body))
}