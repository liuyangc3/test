package http

import (
	"testing"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
	"net"
	"context"
)

var port = ":8080"

func TestHandle(t *testing.T) {
	// this not work because http.Handle need
	// interface http.Handler as second argument
	//http.Handle("/", func(w http.ResponseWriter, r *http.Request) {
	//	w.Write([]byte("Hello World"))
	//})

	var handler http.HandlerFunc = func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Test http.Handle"))
	}
	http.Handle("/", handler)

	_ = http.ListenAndServe(port, nil)
}

// go test http\http_test.go -run TestHandleFunc
func TestHandleFunc(t *testing.T) {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Test http.HandleFunc"))
	})

	_ = http.ListenAndServe(port, nil)
}

// go test http\http_test.go -run TestServeMux
func TestServeMux(t *testing.T) {
	mux := http.NewServeMux()

	// use mux.Handle() is same
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Test mux.ServeMux"))
	})
	_ = http.ListenAndServe(port, mux)
}

// go test http\http_test.go -run TestHttpServer
func TestHttpServer(t *testing.T) {
	var handler http.HandlerFunc = func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("TestHttpServer"))
	}

	// just what does http.ListenAndServe do
	server := &http.Server{
		Handler:      http.HandlerFunc(handler), // interface http.Handler ServeHTTP
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

// Graceful stop
// https://github.com/facebookgo/httpdown
// https://gist.github.com/peterhellberg/38117e546c217960747aacf689af3dc2

// new in go 1.8 func (srv *Server) Shutdown(ctx context.Context) error

// go test http\http_test.go -run TestSignalStop
func TestSignalStop(t *testing.T) {
	var signalChan = make(chan os.Signal)
	signal.Notify(signalChan, os.Interrupt, syscall.SIGTERM)
	signal.Notify(signalChan, syscall.SIGINT)

	var handler http.HandlerFunc = func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("TestSignalStop"))
	}

	server := &http.Server{Addr: port, Handler: handler}

	go func() {
		println("Listening on http://0.0.0.0%s\n", port)
		if err := server.ListenAndServe(); err != nil {
			t.Fatal(err)
		}
	}()

	<-signalChan
	ctx, _ := context.WithTimeout(context.Background(), 1*time.Second)
	println("stop server 1 second after")
	server.Shutdown(ctx)

}

// go test http\http_test.go -run TestHijack
func TestHijack(t *testing.T) {

	http.HandleFunc("/hijack", func(w http.ResponseWriter, r *http.Request) {
		hj, ok := w.(http.Hijacker)
		if !ok {
			http.Error(w, " Hijacker error", http.StatusInternalServerError)
			return
		}

		conn, buf, err := hj.Hijack()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer conn.Close()
		// can not use w.Write
		// http: response.Write on hijacked connection
		w.Write([]byte("hello"))

		// in TCP
		buf.WriteString("Test Hijack")
		buf.Flush()
	})

	_ = http.ListenAndServe(port, nil)
}

// http.ResponseWriter.Flush()  ???
