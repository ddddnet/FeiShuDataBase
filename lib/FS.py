import requests
import json
#ddddnet@https://github.com/ddddnet/FeiShuDataBase
class FS_APP():#飞书自建应用
    def __init__(self,APP_ID,APP_SECRET):
        """
        :param APP_ID: 自建应用的APP_ID
        :param APP_SECRET: 自建应用的APP_SECRET
        """
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET
    
    # 自建应用获取tenant_access_token
    def __get_tenant_access_token(self):
        msg = {
            "code": 400,
            "msg": "get_tenant_access_token fail",
            "data": ""
        }
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = json.dumps({
            "app_id": self.APP_ID,
            "app_secret": self.APP_SECRET
        })
        headers = {
            'Content-Type': 'application/json',
        }
        # 防止网络错误
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            #网络错误
            if response.status_code != 200:
                msg["code"] = 4001
                msg["msg"] = "Network Error"
                msg["data"] = response.text
                return dict(msg)
        except Exception as e:
                #其他错误
                msg["code"] = 4002
                msg["msg"] = str(e)
                return dict(msg)
        
        data = json.loads(response.text)
        if data.get("code") == 0:
            msg["code"] = 0
            msg["msg"] = "get_tenant_access_token success"
            msg["tenant_access_token"] = data.get('tenant_access_token')
            msg["data"] = data
            return dict(msg)
        else:
            msg["code"] = 4003
            msg["msg"] = "get_tenant_access_token fail"
            msg["data"] = data
            return dict(msg)
        
    def tenant_access_token(self):
         data = self.__get_tenant_access_token()
         try:
             return data.get("tenant_access_token")
         except Exception as e:
             return e

        
class   FS_Table():# 飞书多维表格
    def __init__(self,tenant_access_token,APP_TOKEN,TABLE_ID):
        """
        :param APP_TOKEN: 多维表格的APP_TOKEN
        :param TABLE_ID: 数据表的TABLE_ID
        """
        self.tenant_access_token = tenant_access_token
        self.APP_TOKEN = APP_TOKEN
        self.TABLE_ID = TABLE_ID
        self.__where_value = None
    
    # ✅增 多维表格中的数据表插入记录
    def add(self,fields):
        '''
        多维表格中的数据表插入记录
        :fields(dict): 插入的内容如下：
        {
		    "A": "ABC",
		    "B": "234"
	    }
        '''
        msg = {
        "code": 500,
        "msg": "fail",
        "data": ""
        }
        APP_TOKEN = self.APP_TOKEN
        TABLE_ID = self.TABLE_ID
        tenant_access_token = self.tenant_access_token
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps/"+APP_TOKEN+"/tables/"+TABLE_ID+"/records"
        try:
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+tenant_access_token
            }
            payload = json.dumps({
                "fields": fields
            })
        except Exception as e:
            msg["code"] = 5004
            msg["msg"] = "json.dumps fail or tenant_access_token fail"
            msg["data"] = str(e)
            return msg
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            if result.get("code") == 0:
                msg["code"] = 0
                msg["msg"] = "success"
                msg["data"] = result.get("data")
                return msg
            else:
                msg["code"] = 5002
                msg["msg"] = "add_user fail"
                msg["data"] = result
                msg["error_code"] = result.get("code")
                return msg
        except Exception as e:
            msg["code"] = 5003
            msg["msg"] = e
            return msg
    
    def where(self,where_value):
        '''
        多维表格中的数据表查询记录
        :where_value[]: 查询的内容 
        [
            {
                "field_name": "字段名1",
                "operator": "is",(等于)
                "value": ["字段值1"]
            },
            {
                "field_name": "字段名2",
                "operator": "isNot",(不等于)
                "value": ["字段值2"]
            }
        ]
        '''
        self.__where_value = where_value
        return self
    
    def get(self):
        
        value = self.__where_value
        msg = {
        "code": 600,
        "msg": "fail",
        "data": ""
        }
        APP_TOKEN = self.APP_TOKEN
        TABLE_ID = self.TABLE_ID
        tenant_access_token = self.tenant_access_token
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps/"+ APP_TOKEN +"/tables/"+ TABLE_ID +"/records/search"
        conjunction = "and" # 精确查询使用and（满足全部条件） 模糊查询使用or（满足任一条件）
        
        # 处理传入数据中operator为空的情况，设置默认值为"is"
        for condition in value:
            if "operator" not in condition or not condition["operator"]:
                condition["operator"] = "is"
        
        try:
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+tenant_access_token
            }
            payload = json.dumps({
	            "filter": {
		        "conditions": value,
		        "conjunction": conjunction
	            }
            })
        except Exception as e:
            msg["code"] = 6004
            msg["msg"] = "json.dumps fail or tenant_access_token fail"
            msg["data"] = str(e)
            return msg
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            if result.get("code") == 0:
                msg["code"] = 0
                msg["msg"] = "success"
                msg["data"] = result.get("data")
                return msg
            else:
                msg["code"] = 6002
                msg["msg"] = "where fail"
                msg["data"] = result
                msg["error_code"] = result.get("code")
                return msg
        except Exception as e:
            msg["code"] = 6003
            msg["msg"] = e
            return msg
        
    def remove(self):
        msg = {
        "code": 700,
        "msg": "fail",
        "data": ""
        }
        APP_TOKEN = self.APP_TOKEN
        TABLE_ID = self.TABLE_ID
        tenant_access_token = self.tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps/"+APP_TOKEN+"/tables/"+TABLE_ID+"/records/batch_delete"
        
        
        get_data = self.get()
        items = get_data.get("data").get("items")
        record_ids = []
        for i in items:
            record_id = i.get("record_id")
            record_ids.append(record_id)
        
        
        try:
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+tenant_access_token
            }
            payload = json.dumps({
	            "records": record_ids
            })
        except Exception as e:
            msg["code"] = 7004
            msg["msg"] = "json.dumps fail or tenant_access_token fail"
            msg["data"] = str(e)
            return msg
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            if result.get("code") == 0:
                msg["code"] = 0
                msg["msg"] = "success"
                msg["data"] = result.get("data")
                return msg
            else:
                msg["code"] = 7002
                msg["msg"] = "remove fail"
                msg["data"] = result
                msg["error_code"] = result.get("code")
                return msg
        except Exception as e:
            msg["code"] = 7003
            msg["msg"] = e
            return msg
        
        
    def update(self,fields):
        msg = {
        "code": 800,
        "msg": "fail",
        "data": ""
        }
        APP_TOKEN = self.APP_TOKEN
        TABLE_ID = self.TABLE_ID
        tenant_access_token = self.tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps/"+APP_TOKEN+"/tables/"+TABLE_ID+"/records/batch_update"
        
        get_data = self.get()
        items = get_data.get("data").get("items")
        record_ids = []
        for i in items:
            record_id = i.get("record_id")
            record_ids.append(record_id)
        
        # 构造records列表，将每个record_id和对应的fields组合起来
        records = []
        for index in range(len(record_ids)):
            record_info = {
                "record_id": record_ids[index],
                "fields": fields  # 防止fields长度不足时出错
            }
            records.append(record_info)
        
        payload = json.dumps({
            "records": records
        })
        
        try:
            # 构造records列表，将每个record_id和对应的fields组合起来
            records = []
            for index in range(len(record_ids)):
                record_info = {
                    "record_id": record_ids[index],
                    "fields": fields  # 防止fields长度不足时出错
                }
                records.append(record_info)
        
            payload = json.dumps({
                "records": records
            })
            
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+tenant_access_token
            }
            
        except Exception as e:
            msg["code"] = 8004
            msg["msg"] = "json.dumps fail or tenant_access_token fail record_ids fail"
            msg["data"] = str(e)
            return msg
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            if result.get("code") == 0:
                msg["code"] = 0
                msg["msg"] = "success"
                msg["data"] = result.get("data")
                return msg
            else:
                msg["code"] = 8002
                msg["msg"] = "update fail"
                msg["data"] = result
                msg["error_code"] = result.get("code")
                return msg
        except Exception as e:
            msg["code"] = 7003
            msg["msg"] = e
            return msg
        
        
        