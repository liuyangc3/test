# easyarray
Opereate shell array like Python list .

to make operating array in shell easier.

## get easyarray
```
wget https://raw.githubusercontent.com/liuyangc3/test/master/shell/easyarray
```
## example
```
#!/bin/sh
# source easyarray
. /path-to-script/easyarray

foo=(1 2 3)

# init, turn shell array into easyarray
easyarray_init foo 

# append item
foo_append "x"

# echo array
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
get index of item, index start with `0`

return `""` if item not in array  
```
foo=(a b foo c)
foo_index "foo"
----
2
```
have fun


# render.sh
a simple temlate engine write by shell

# remote_cmd.sh
execute shell command on a remote host
