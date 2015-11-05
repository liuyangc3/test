# easyarray
Opereate shell array like Python list .

to make operating array in shell easier.

## install
```
wget https://raw.githubusercontent.com/liuyangc3/easy-shell-array/master/easyarray
```
## example
```
#!/bin/sh
. /path-to-script/easyarray

foo=(1 2 3)

easyarray_init foo # init a array
foo_append "x"
foo_echo
----
1 2 3 x
```
get length of array
```
foo_len
----
4
```
pop last item
```
foo_pop
foo_len
foo_echo
----
x
3
1 2 3
```
find item index, get "" if item not in array 
```
foo=(a b "hello world" c)
foo_index "hello world"
----
2
```
have fun
