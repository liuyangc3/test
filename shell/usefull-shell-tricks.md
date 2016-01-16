# String
## lower to upper
```
echo $VAR | sed 's/\(.\)/\U\1/g'   # \(.\) match single character 
tr '[a-z]' '[A-Z]' <<< "$VAR"
echo $VAR | tr '[:lower:]' '[:upper:]'
```
## upper to lower
```
sed 's/\(.\)/\l\1/g' <<< "$VAR"
tr '[A-Z]' '[a-z]' <<< $VAR
echo $VAR | tr '[:upper:]' '[:lower:]'
```

## split
```
input=abc.xyz
while IFS='.' read -ra array; do
      for i in "${array[@]}"; do
          # process "$i"
      done
 done <<< "$input"
 
# or
array=(${input//./ })
```
## parse key and value 
string format `key=value`
```
input="foo=bar"
sed -e 's/=.*$//' <<< "$input"     # get key 
sed -e 's/^[^=]*=//' <<< "$input"  # get value
```

# echo tabs in string
use `$` + `string`
```
echo Hello$'\t'world
Hello   world
```

# math
```
i=1
((i++))  # i=i+1
echo $i
2
let i=i+3
echo $i
4
echo '1/2'|bc
0
echo '1/2'|bc -l
.50000000000000000000
echo 'scale=3;1/2'|bc
.500
```

# Shell internal
## show shell variables
```
(set -o posix;set)  #  show keys and values
compgen -A variable # show keys without value
compgen -v  # short for -A variable
```

## show user define variables
```
(set -o posix;set)|xargs -d'\n'|grep -oP '(?<=_=posix ).*'
```


# Other
# use fd to send tcp package
```
exec 6<>/dev/tcp/127.0.0.1/2181  # assign fd 6 to tcp sokect file
echo ruok>&6   # wirte
read -n 4 <&6  # read 4 characters
cat <&6        # read all
exec 6>&-      # close fd
```


# timestamp conver to date
```
ts=1451633323
date -d "@$ts" +"%F %H:%M:%S"
2016-01-01 15:28:43
```
# date conver to timestamp
```
date="2016-01-01 15:28:43"
date -d "$date" +%s
1451633323
```
