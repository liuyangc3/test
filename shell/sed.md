# 匹配行到最后一行(包括匹配行)
sed -n  '/${partten}/,$p' file


# 显示匹配行到最后一行(不包括匹配行)
sed -n '/regx/,${//!p}' file

# 仅显示堆栈信息(以 space 开头) 
sed -n '/${partten}/,/^$/p' file

# 删除空行
sed '/^$/d' file

# 显示匹配行到最后一行(不包括匹配行) 并删除空行
sed -n '/${partten}/,${//!p;/^$/d}' file

