package sync

import (
	"testing"
	"sync"
)

func TestSyncOnce(t *testing.T) {

	var o sync.Once
	o.Do(func() {
		t.Log("do once")
	})
}