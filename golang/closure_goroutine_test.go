package main

import (
	"testing"
	"sync"
)

// https://golang.org/doc/faq#closures_and_goroutines

func TestSign(_ *testing.T) {
	values := []string{"a", "b", "c"}
	var wg sync.WaitGroup
	wg.Add(len(values))
	for i, v := range values {
		v := v // create a new 'v'.
		println(&values[i])
		go func() {
			println(v, &v)
			wg.Done()
		}()
	}
	println("done")
	wg.Wait()
}

