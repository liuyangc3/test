package main

import "testing"

func TestStringPointerAdd(t *testing.T) {
	a := "test"
	b := "1"
	ap := &a
	bp := &b

	v := *ap + *bp
	ap = &v
	println(*ap)

}

