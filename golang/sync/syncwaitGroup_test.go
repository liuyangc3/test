package sync

import (
	"sync"
	"time"
	"math/rand"
	"fmt"
	"testing"
)

func TestMain(m *testing.M) {
	// setup
	rand.Seed(time.Now().Unix())
	m.Run()
	// teardown
}


func TestNoWait(t *testing.T) {
	go func() {
		num := rand.Int31n(10)
		fmt.Println("sleep %d second", num)
		time.Sleep(time.Duration(num) * time.Second)
		println("goroutine done")
	}()
	println("mian done")
}

func TestWaitGroup(t *testing.T) {
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		num := rand.Int31n(10)
		fmt.Println("sleep %d second", num)
		time.Sleep(time.Duration(num) * time.Second)
		wg.Done()
		println("goroutine done")
	}()
	wg.Wait()
	println("mian done")
}

