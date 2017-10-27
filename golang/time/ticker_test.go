package time

import (
	"testing"
	"time"
	"sync"
)

// go test -v "time\ticker_test.go" -run TimeTicker2

func TestTimeTicker(t *testing.T) {
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		for t := range ticker.C {
			println(1, t.String())
			//wg.Done()   main thread will not stop
		}
	}()

	wg.Wait()
}

func TestTimeTicker2(t *testing.T) {
	// time.Tick is simple version of NewTicker
	// and can not stop

	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		for t := range time.Tick(time.Second) {
			println(2, t.String())
			//wg.Done()   main thread will not stop
		}
	}()

	wg.Wait()
}
