from lib.FS import FS_APP, FS_Table

# 这是一个测试用的示例代码，你可以根据自己的需求进行修改。
# 仓库地址https://github.com/ddddnet/FeiShuDataBase

APP_ID = "cli_a7eb38b997b8500e" #自建应用ID
APP_SECRET = "jI6Ond098BEHKa8OeOoDVgmfttYWPP1T" #自建应用密钥

APP_TOKEN = "JVahbRGYDa2UDUs98usctpDYnVe" #多维表格ID
TABLE_ID = "tblCOZDgMbbFj4A6" #数据表ID

app = FS_APP(APP_ID,APP_SECRET)
tenant_access_token = app.tenant_access_token()

table = FS_Table(tenant_access_token,APP_TOKEN,TABLE_ID)

if __name__ == "__main__":
    
    # ✅新增记录
    fidels = {
		    "ID": "1",
		    "key": "key",
            "value": "value",
	    }
    data1 = table.add(fidels)
    print(data1)
    
    # ✅查询记录
    data2 = table.where([
        {
            "field_name": "ID",
            "operator": "is",
            "value": ["1"]
        }
    ]).get()
    print(data2)
    
    # ✅简单查询
    data3 = table.where([
        {
            "field_name": "ID",
            "value": ["1"]
        }
    ]).get()
    print(data3)
    
    # ✅删除记录 where查询后有多条记录 则.remove会把多条记录删除
    data4 = table.where([
        {
            "field_name": "value",
            "value": ["new value"]
        }
    ]).remove()
    
    print(data4)
    
    # ✅update
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
    
    
    copyright = 'ddddnet@github'