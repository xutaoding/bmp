# coding: utf-8
USER_SESSION = "user"

REFS = {
    "项目名称": ["ichinascope", "chinascopefinancial", "智投", "数库云", "数库港", "后台系统"],
    "数据库": ["mongodb", "mysql", "oracle", "sqlserver"],
    "web": ["PHP", "Nginx", "Apache", "other"],
    "应用服务": ["portalmobile", "ada", "datafeed", "datashift", "datareceiver", "datacloud", "hqservice", "csdata",
             "otcds", "bts", "shukugang", "idexservice", "indexer"],
    "服务": ["数据库", "web", "应用服务"],
    "地点": ["办公室", "上海IDC", "亚马逊(北京)", "亚马逊(新加坡)"],
    "审批": ["内部测试", "运维发布", "正式环境测试"],
    "未通过原因": ["BUG", "文件未成功修改", "数据问题", "配置文件错误", "问题未修改", "发布问题", "其他"],
    "库存状态": ["领用", "借用", "维修", "报废"],
    "入库类型": ["采购入库", "其它入库"]
}


class DEFAULT_GROUP:
    QA = "QA"
    OP = "OP"
    GUEST = "GUEST"
    GROUPS = {
        "QA": ["KIKI.zhang", "aurora.yang", "helen.yang"],
        "OP": ["ryan.wang", "jim.zhao"],
        "GUEST": []
    }


class RELEASE:
    PASS = u"已确认"
    FAIL = u"退回"
    FLOW_OP = [u"运维发布"]
    FLOW_QA = [u"内部测试", u"正式环境测试"]


class PURCHASE:
    PASS = u"已确认"
    FAIL = u"退回"
    FLOW_ONE = "UP"
    FLOW_TWO = "FIN"
    FLOW_THREE = "BOSS"
    FLOW_FOUR = "LAW"
    FLOW = [FLOW_ONE, FLOW_TWO, FLOW_THREE, FLOW_FOUR]
    PRICE_LIMIT = 10000

class SCRAP:
    PASS = u"已确认"
    FAIL = u"退回"
    TYPE = u"报废"



if __name__ == "__main__":
    pass
