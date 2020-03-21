# PQL设计说明
## 一、语言设计
**采用类似sql语言的解析过程设计本语言，用于基于差分保护的数据查询。**
具体PQL语法如下：  

```
PROTECT  protect_ table|name
PICK  pick_fun|column
WITH  with_specific   
[OR WITHRANGE(X,Y)  withrange(x,y)_range of ]
[Global  global_global sensitivity + [WHERE  where_condition ]]
[ WHERE  where_condition ]
```

## 二、设计说明
### 1.关键字：protect、pick、with必选，global、where可选
* **protect:** 需要查询的表，类似sql中的from
* **pick:** 需要使用的函数，类似sql中的select  
* **with:** 需要添加差分噪声ε值
* **withrange:** 需要添加差分噪声ε区间
* **global:** 全局敏感度，非必选关键词
* **where:** 条件查询，非必选关键词
### 2.多条件连接字符：and/or连接
### 3.运算符：运算符为常规通用运算符（> < <> =）对应为大于、小于、不等于、等于
### 4.支持函数：
```
    avg[column_name]——平均
    total[column_name]——总和
    highest[column_name]——最大值
    lowest[column_name]——最小值
    count[*]——行数
```
对应sql函数：**avg()、sum()、max()、min()、count()**
### 5.错误处理：
* 关键字拼写错误、必选关键字少些货或多写报错，可选关键字多写报错
* 条件连接字符报错规则与sql一致
* 运算符报错规则与sql一致
* 函数除`count[]`函数外，其他函数`[]`内必须且只能写入一个字段，否则报错，`count[]`函数`[]`内需填写`*`，即`count[*]`，其他写法报错
* 其他表或字段拼写错误报错规则与sql一致
## 三、实例

现有表`expenses`,字段有`day`、`total`  

* 我们查询`day`大于5，差分ε为0.1的统计，写法如下：
```
protect expenses pick count[*] with 0.1 where day>5
```
* 我们查询`total`大于500且`day`小于10的`total`平均值，差分ε为0.8的统计，写法如下：
```
protect expenses pick avg[total] with 0.8 where total>500 and day<10
```