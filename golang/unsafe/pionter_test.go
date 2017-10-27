package unsafe

import (
	"testing"
	"unsafe"
)

type S struct {}

type byte8 struct {
	u uint64
}
type byte16 struct {
	e byte8
	u uint64
}

func TestPointer(_ *testing.T) {
	var u uint64
	println(unsafe.Sizeof(u))

	var s S
	println(unsafe.Sizeof(s))   // 0
	println(unsafe.Sizeof(S{}))

	var b16 byte16
	println(unsafe.Sizeof(b16))
	println(unsafe.Sizeof(byte16{}))

}
