package runtime

import (
	"runtime"
	"testing"
	"reflect"
	"time"
)

// go test runtime\memory_test.go -run TestMemStats -v
func TestMemStats(t *testing.T) {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)

	v := reflect.ValueOf(&m).Elem()

	for i := 0; i < v.NumField(); i++ {
		t.Logf("%s %s %v \n",
			v.Field(i).Type(),
			v.Type().Field(i).Name,
			v.Field(i).Interface())
	}
}




// go test runtime\memory_test.go -run TestMemProfile -v
func TestMemProfile(t *testing.T) {
	_ = make([]byte, 5000000)

	var mprs []runtime.MemProfileRecord
	n, ok := runtime.MemProfile(mprs, true)
	for {
		// Allocate room for a slightly bigger profile,
		// in case a few more entries have been added
		// since the call to MemProfile.
		mprs = make([]runtime.MemProfileRecord, n+50)
		n, ok = runtime.MemProfile(mprs, true)
		if ok {
			mprs = mprs[0:n]
			break
		}
		// Profile grew; try again.
	}

	var total runtime.MemProfileRecord
	for i := range mprs {
		r := &mprs[i]
		total.AllocBytes += r.AllocBytes
		total.AllocObjects += r.AllocObjects
		total.FreeBytes += r.FreeBytes
		total.FreeObjects += r.FreeObjects
	}

	t.Logf(`
	AllocBytes: %d
	AllocObjects: %d
	FreeBytes: %d
	FreeObjects: %d
	InUseObjects: %d
	InUseBytes: %d
	Stack: %v
	`,
		total.AllocBytes,
		total.AllocObjects,
		total.FreeBytes,
		total.FreeObjects,
		total.InUseObjects(),
		total.InUseBytes(),
		total.Stack())
}

// go test runtime\memory_test.go -run TestSetFinalizer -v
// https://golang.org/pkg/runtime/#hdr-Environment_Variables
// GODEBUG="gctrace=1" && go test runtime\memory_test.go -run TestSetFinalizer -v
func TestSetFinalizer(t *testing.T) {

	var a, b []string
	runtime.SetFinalizer(&a, func(*[]string) {println("Finalizer in a")})
	runtime.SetFinalizer(&b, func(*[]string) {println("Finalizer in b")})

	for i:=0;i<3;i++ {
		println("gc", i)
		runtime.GC()
		time.Sleep(time.Second)
	}
}