package http

import (
	"fmt"
	"io/ioutil"
	"testing"
	"net/http"
)

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