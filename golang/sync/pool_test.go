package sync

import (
	"sync"
	"testing"
)

type T struct {
	name string
}

var pool = &sync.Pool{}

func TestPool(t *testing.T) {
	a := &T{name: "a"}
	pool.Put(a)
	x := pool.Get().(*T)
	println(a, x) // address should be same

	// put it back
	pool.Put(x)
}

func TestPool2(t *testing.T) {
	x := pool.Get().(*T)
	println(x)
}