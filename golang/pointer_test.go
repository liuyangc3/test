package main

import (
	"testing"
	"reflect"
	"unsafe"
)

func TestPointer(t *testing.T) {
	v1 := uint(10)
	v2 := int(100)

	t.Log(reflect.TypeOf(v1), reflect.TypeOf(v2))
	t.Log(reflect.TypeOf(&v1), reflect.TypeOf(&v2))

	p := &v1
	p = (*uint)(unsafe.Pointer(&v2)) //使用unsafe.Pointer进行类型的转换
	t.Log(reflect.TypeOf(p), *p)
}

func TestPointerOffset(t *testing.T) {
	var s struct {
		a bool
		b int16
		c []int
	}

	p := (*int16)(unsafe.Pointer(uintptr(unsafe.Pointer(&s)) + unsafe.Offsetof(s.b)))
	*p = 10
	t.Log(s.b)
}
