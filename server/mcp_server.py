# 全局导入
import json
import os
from hashlib import md5
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys

load_dotenv()

mcp = FastMCP("专利大数据", instructions="专利大数据",dependencies=["python-dotenv", "requests"])

INTEGRATOR_ID = os.environ.get("INTEGRATOR_ID")
SECRET_ID = os.environ.get("SECRET_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")

def call_api(product_id: str, params: dict) -> dict:
    """
    调用API接口
    
    参数:
      - product_id: 数据产品ID
      - params: 接口参数
    
    返回:
      - 接口返回的JSON数据
    """
    if not params:
        params = {}
    
    if not INTEGRATOR_ID:
        return {"error": "对接器ID不能为空"}
    
    if not SECRET_ID:
        return {"error": "密钥ID不能为空"}
    
    if not SECRET_KEY:
        return {"error": "密钥不能为空"}
    
    if not product_id:
        return {"error": "产品ID不能为空"}
    
    call_params = {
        "product_id": product_id,
        "secret_id": SECRET_ID,
        "params": json.dumps(params, ensure_ascii=False)
    }
    
    # 生成签名
    keys = sorted(list(call_params.keys()))
    params_str = ""
    for key in keys:
        params_str += str(call_params[key])
    params_str += SECRET_KEY
    sign = md5(params_str.encode("utf-8")).hexdigest()
    call_params["signature"] = sign
    
    # 调用API
    url = f'https://console.handaas.com/api/v1/integrator/call_api/{INTEGRATOR_ID}'
    try:
        response = requests.post(url, data=call_params)
        return response.json().get("data", None) or response.json().get("msgCN", None)
    except Exception as e:
        return "查询失败"
    
@mcp.tool()
def patent_bigdata_patent_search(matchKeyword: str, pageSize: int = 10, patentType: str = None, keywordType: str = None,
                  pageIndex: int = None) -> dict:
    """
    该接口的功能是提供专利信息的搜索服务，通过输入专利名称、申请号、申请人或代理机构等信息进行精准或模糊搜索，并按指定的专利类型进行筛选，返回符合条件的专利详细信息列表。这个接口的使用场景包括：专利代理机构通过该接口获取竞争对手的专利布局情况，研发人员查找特定领域的已有专利以规避侵权，或者企业在技术创新过程中进行专利情报分析，以便判断市场竞争态势和寻找合作机会。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 专利名称/专利申请号/公布公告号/申请人/代理机构
    - pageSize: 分页大小 类型：int - 一页最多获取50条数据
    - patentType: 专利类型 类型：select - 专利类型枚举（发明申请，实用新型，发明授权，外观设计）
    - keywordType: 搜索方式 类型：select - 搜索方式枚举（专利名称，申请号/公开号，申请人，代理机构)，默认全部匹配
    - pageIndex: 页码 类型：int - 从1开始

    返回参数:
    - resultList: 结果列表 类型：list of dict
    - _id: 专利id 类型：string
    - calPatentLegalStatus: 专利状态 类型：string
    - patentAgency: 代理机构 类型：string
    - patentAgencyNameId: 代理机构id 类型：string
    - patentApplicantName: 申请人名称 类型：string
    - patentApplicationDate: 专利申请日期 类型：string
    - patentApplicantNameId: 申请人id 类型：string
    - patentIPC: IPC分类号 类型：list of str
    - patentName: 专利名称 类型：string
    - patentApplicationNum: 专利申请号 类型：string
    - patentPubNum: 专利公告号 类型：string
    - patentPubDate: 专利公告日期 类型：string
    - patentType: 专利类型 类型：string
    - total: 总数 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageSize': pageSize,
        'patentType': patentType,
        'keywordType': keywordType,
        'pageIndex': pageIndex,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66b338e274bf098447db7f37', params)


@mcp.tool()
def patent_bigdata_patent_stats(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口的功能是根据提供的企业信息查询企业的专利情况，包括专利状态分布、专利申请与授权趋势、以及按专利类型分布的专利数量等。此接口可用于企业内部专利管理与分析、行业竞争态势研究、以及投资者评估企业创新能力和技术储备时的数据支持。通常适用于需要了解企业在专利方面详细布局的场景，如市场分析、科技项目评估、以及法律诉讼风险评估等。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - patentDivAppLegalStat: 专利状态分布 类型：list of dict
    - patentCount: 专利数量 类型：int
    - patentDivAppLegal: 专利状态名称 类型：string
    - patentTypeAppTimeStat: 专利申请趋势 类型：list of dict
    - appearanceDesignPatentCount: 外观设计专利数量 类型：int
    - inventionLicPatentCount: 发明授权专利数量 类型：int
    - inventionAppPatentCount: 发明申请专利数量 类型：int
    - year: 年份 类型：string
    - patentTypePubTimeStat: 专利授权趋势 类型：list of dict
    - inventionAppPatentCount: 发明申请专利数量 类型：int
    - inventionLicPatentCount: 发明授权专利数量 类型：int
    - utilityModelPatentCount: 实用新型专利数量 类型：int
    - utilityModelPatentCount: 实用新型专利数量 类型：int
    - appearanceDesignPatentCount: 外观设计专利数量 类型：int
    - year: 年份 类型：string
    - inventionAppPatentCount: 发明申请专利数量 类型：int
    - inventionLicPatentCount: 发明授权专利数量 类型：int
    - utilityModelPatentCount: 实用新型专利数量 类型：int
    - appearanceDesignPatentCount: 外观设计专利数量 类型：int
    - patentTypeStat: 专利类型分布 类型：dict
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66d5b7df537c3f61d646c230', params)


@mcp.tool()
def patent_bigdata_fuzzy_search(matchKeyword: str, pageIndex: int = 1, pageSize: int = None) -> dict:
    """
    该接口的功能是根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。返回匹配的企业列表及其详细信息，用于查找和识别特定的企业信息。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 查询各类信息包含匹配关键词的企业
    - pageIndex: 分页开始位置 类型：int
    - pageSize: 分页结束位置 类型：int - 一页最多获取50条数据

    返回参数:
    - total: 总数 类型：int
    - resultList: 结果列表 类型：list of dict
    - annualTurnover: 年营业额 类型：string
    - formerNames: 曾用名 类型：list of string
    - address: 注册地址 类型：string
    - foundTime: 成立时间 类型：string
    - enterpriseType: 企业主体类型 类型：string
    - legalRepresentative: 法定代表人 类型：string
    - homepage: 企业官网 类型：string
    - legalRepresentativeId: 法定代表人id 类型：string
    - prmtKeys: 推广关键词 类型：list of string
    - operStatus: 企业状态 类型：string
    - logo: 企业logo 类型：string
    - nameId: 企业id 类型：string
    - regCapitalCoinType: 注册资本币种 类型：string
    - regCapitalValue: 注册资本金额 类型：int
    - name: 企业名称 类型：string
    - catchReason: 命中原因 类型：dict
    - catchReason.name: 企业名称 类型：list of string
    - catchReason.formerNames: 曾用名 类型：list of string
    - catchReason.holderList: 股东 类型：list of string
    - catchReason.recruitingName: 招聘岗位 类型：list of string
    - catchReason.address: 地址 类型：list of string
    - catchReason.operBrandList: 品牌 类型：list of string
    - catchReason.goodsNameList: 产品名称 类型：list of string
    - catchReason.phoneList: 固话 类型：list of string
    - catchReason.emailList: 邮箱 类型：list of string
    - catchReason.mobileList: 手机 类型：list of string
    - catchReason.patentNameList: 专利 类型：list of string
    - catchReason.certNameList: 资质证书 类型：list of string
    - catchReason.prmtKeys: 推广关键词 类型：list of string
    - catchReason.socialCreditCode: 统一社会信用代码 类型：list of string

    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('675cea1f0e009a9ea37edaa1', params)


if __name__ == "__main__":
    print("正在启动MCP服务...")
    # 解析第一个参数
    if len(sys.argv) > 1:
        start_type = sys.argv[1]
    else:
        start_type = "stdio"

    print(f"启动方式: {start_type}")
    if start_type == "stdio":
        print("正在使用stdio方式启动MCP服务器...")
        mcp.run(transport="stdio")
    if start_type == "sse":
        print("正在使用sse方式启动MCP服务器...")
        mcp.run(transport="sse")
    elif start_type == "streamable-http":
        print("正在使用streamable-http方式启动MCP服务器...")
        mcp.run(transport="streamable-http")
    else:
        print("请输入正确的启动方式: stdio 或 sse 或 streamable-http")
        exit(1)
    