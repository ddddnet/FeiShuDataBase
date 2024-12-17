# 免费可视数据库-python连接飞书多维表格

## ***连接飞书多维表格的python库*** ***简短代码实现`增、删、查、改`***

## 👉[文档地址](https://gcn2ovxcjfar.feishu.cn/docx/CQ3OdTsWnoLbEix67g3c60TVnjh)

**[飞书多维表格](https://docs.feishu.cn/)支持数据定制** **表格**、**甘特图**、**画册**、**看板**  **等多种视图，零代码轻松封装后台业务应用**

多维表格可以创建很多个数据表，我们的程序可以把数据接入到多维表格中，实现免费的数据库，并且多维表格的视图功能非常丰富，可以0代码自建多种后台视图，数据管理还能使用AI功能，智能化提取分析数据。👉[多维表格介绍](https://www.feishu.cn/content/multidimensional-table-guide)



```Python
table.add({"fidel" : "value","key" : "value"})
一行代码实现新增数据记录
```



# 一、初始化教程



## 1.导入文件

- 把`lib/FS.py` 放到项目
- 在项目中导入FS.py文件 

```Python
from lib.FS import FS_APP, FS_Table
```



## 2.选择自建应用

自建应用是用来操作表格数据的，有了它我们才有权限读写数据，类似于后台管理员。

而选择自建应用相当于选择管理员A或管理员B的身份来操作，每个应用的权限可能会不一样，所以能够有效做到安全隔离。

- 首先需要新建自建应用👉[教程](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#VQbTdRIMUomcvoxWRZAcbaxwnSc)
- 获取APP_ID 与 APP_SECRET👉[教程](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#YkX7dFt5Ro9fBOxBoN5cWY0lnWb)

```Python
APP_ID = "cli_a7eb38b997b8500e" #自建应用ID
APP_SECRET = "jI6Ond098BEHKa8OeOoDVgmfttYWPP1T" #自建应用密钥

app = FS_APP(APP_ID,APP_SECRET) #选择一个自建应用
tenant_access_token = app.tenant_access_token() #获得临时密钥
```



## 3.选择多维表格

多维表格相当于数据库（APP_TOKEN)，而数据库里面有很多数据表(TABLE_ID)。

操作多维表格需要临时密钥（tenant_access_token）

- 首先需要新建多维表格👉[教程](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#KqmudsQTUoMetJxBfHXcYjDNn8e)并且授权应用可操作表格👉[教程](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#E7y0dgofqo8We2xAbMjcYeAjnkg)
- 获取APP_TOKEN与 TABLE_ID👉[教程](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#KCr9dczCIo398mx7MEzcFKRAnpc)

```Python
APP_TOKEN = "JVahbRGYDa2UDUs98usctpDYnVe" #多维表格ID
TABLE_ID = "tblCOZDgMbbFj4A6" #数据表ID

table = FS_Table(tenant_access_token,APP_TOKEN,TABLE_ID) #数据表

# 可以操作多个数据表
TABLE_ID1 = "tbloPqOWrCsapVLS" #数据表1 ID
table1 = FS_Table(tenant_access_token,APP_TOKEN,TABLE_ID) #数据表1
```



# 二、用法



## 新增数据

```
.add()
```

新增字段直接在括号内传入健跟值即可 .add({`"健"："值"`})

例：

```Python
fidels = {
            "ID": "1",
            "key": "key",
            "value": "value",
        }
data1 = table.add(fidels)
print(data1)
```

效果如下：

| ID   | key  | value |
| ---- | ---- | ----- |
| 1    | key  | value |



## 查询并获取数据

先查询`.where()`再获取`.get()`` `

- .where()

`.where`  内传入的是 `[]`,（数据类型：List即列表）


`[]` 列表里可以有很多集合 `{}`


集合是健(key)是固定的`field_name`、`operator`、`value`

| 健         | 类型 | 值                                                           |
| ---------- | ---- | ------------------------------------------------------------ |
| field_name | 文本 | 多维表格中字段的名字                                         |
| operator   | 文本 | 默认值“is”意为“等于”，还有“isnot”等用法，请参考👉[链接](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd#IyScdn9l1oI8csxDYOxcvIdpnNc) |
| value      | 列表 | [1]或["1"] 两个有不同的区别，填写说明👉[链接](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/record-filter-guide#3e0fd644) |

```Python
data2 = table.where([
        {
            "field_name": "ID",
            "operator": "is",
            "value": ["1"]
        }
    ]).get()
print(data2)
```



## 简易查询

默认 `"operator": "is"`

```Python
data3 = table.where([
        {
            "field_name": "ID",
            "value": ["1"]
        }
    ]).get()
print(data3)
```



## 更新字段数据

先查询`.where()`再`.update()`

where查询后有多条记录 则.update会把多条记录的字段更改

```Python
data5 = table.where([
        {
            "field_name": "ID",
            "value": [1]
        }
    ]).update({
        "value": "new value"
        #"字段"："新值"
    })
    
print(data5)
```

**更新前：**

| ID   | key  | value |
| ---- | ---- | ----- |
| 1    | key  | value |

**更新后：**

| ID   | key  | value     |
| ---- | ---- | --------- |
| 1    | key  | new value |



## 删除字段

先查询`.where()`再`.remove()`

where查询后有多条记录 则.remove会把多条记录删除

```Python
data4 = table.where([
        {
            "field_name": "value",
            "value": ["new value"]
        }
    ]).remove()
    
print(data4)
```



# 补充文档

👉[补充文档](https://gcn2ovxcjfar.feishu.cn/docx/V3XfdCr4go4nXqxzddfcOXYmnpd)