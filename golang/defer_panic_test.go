package main

import "testing"

func TestDeferSequence(t *testing.T) {
	// defer register as stack
	// FILO   out -> 3 2 1
	defer println(1)
	defer print(2)
	defer print(3)
}

func TestDeferArgs(t *testing.T) {
	add := func(x, y int) int { return x + y }

	// Args pass by value at runtime
	// so when passing args into defer
	// now a is 1,  b is 3, and add be called
	// out -> 1 3 4
	a := 1
	b := 3
	defer println(a, b, add(a, b))

	// out -> 10 30 40
	a = 10
	b = 30
	defer println(a, b, add(a, b))
}

func f() (r int) {
	defer func() {
		r++
	}()
	return 100
}

func f1() (r int) {
	t := 5
	defer func() {
		t = t + 5
	}()
	return t
}

func f2() (r int) {
	defer func(r int) {
		r = r + 5
	}(r)
	return 1
}

//func TestDeferReturn(t *testing.T) {
//	t.Log(f())
//	t.Log(f1())
//	t.Log(f2())
//}
