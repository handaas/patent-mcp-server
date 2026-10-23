# 专利数据统计

[该MCP服务提供全面的专利信息查询功能，包括专利搜索、专利统计分析等，帮助用户进行专利情报分析、技术创新和知识产权管理。](https://www.handaas.com/)


## 主要功能

- 🔍 企业关键词模糊搜索
- 📄 专利信息搜索
- 📊 企业专利统计分析

## 环境要求

- Python 3.10+
- 依赖包：python-dotenv, requests, mcp

## 本地快速启动

### 1. 克隆项目
```bash
git clone https://github.com/handaas/patent-mcp-server
cd patent-mcp-server
```

### 2. 创建虚拟环境&安装依赖

```bash
python -m venv mcp_env && source mcp_env/bin/activate
pip install -r requirements.txt
```

### 3. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下环境变量：

```env
INTEGRATOR_ID=your_integrator_id
SECRET_ID=your_secret_id
SECRET_KEY=your_secret_key
```

### 4. streamable-http启动服务

```bash
python server/mcp_server.py streamable-http
```

服务将在 `http://localhost:8000` 启动。

#### 支持启动方式 stdio 或 sse 或 streamable-http

### 5. Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "handaas-mcp-server": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## STDIO版安装部署

### 设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "patent-mcp-server": {
      "command": "uv",
      "args": ["run", "mcp", "run", "{workdir}/server/mcp_server.py"],
      "env": {
        "PATH": "{workdir}/mcp_env/bin:$PATH",
        "PYTHONPATH": "{workdir}/mcp_env",
        "INTEGRATOR_ID": "your_integrator_id",
        "SECRET_ID": "your_secret_id",
        "SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

## 使用官方Remote服务

### 1. 直接设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "patent-mcp-server":{
      "type": "streamableHttp",
      "url": "https://mcp.handaas.com/patent/patent_bigdata?token={token}"  
      }
  }
}
```

### 注意：integrator_id、secret_id、secret_key及token需要登录 https://www.handaas.com/ 进行注册开通平台获取


## 可用工具

### 1. patent_bigdata_fuzzy_search
**功能**: 企业关键词模糊查询

根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 查询各类信息包含匹配关键词的企业
- `pageIndex` (可选): 分页开始位置
- `pageSize` (可选): 分页结束位置 - 一页最多获取50条数据

**返回值**:
- `total`: 总数
- 其他企业相关信息

### 2. patent_bigdata_patent_search
**功能**: 专利信息搜索

通过输入专利名称、申请号、申请人或代理机构等信息进行精准或模糊搜索，并按指定的专利类型进行筛选。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 专利名称/专利申请号/公布公告号/申请人/代理机构
- `pageSize` (可选): 分页大小 - 一页最多获取50条数据
- `patentType` (可选): 专利类型 - 发明申请，实用新型，发明授权，外观设计
- `keywordType` (可选): 搜索方式 - 专利名称，申请号/公开号，申请人，代理机构，默认全部匹配
- `pageIndex` (可选): 页码 - 从1开始

**返回值**:
- `resultList`: 专利列表
  - `_id`: 专利id
  - `calPatentLegalStatus`: 专利状态
  - `patentAgency`: 代理机构
  - `patentAgencyNameId`: 代理机构id
  - `patentApplicantName`: 申请人名称
  - `patentApplicationDate`: 专利申请日期
  - `patentApplicantNameId`: 申请人id
  - `patentIPC`: IPC分类号
  - `patentName`: 专利名称
  - `patentApplicationNum`: 专利申请号
  - `patentPubNum`: 专利公告号
  - `patentPubDate`: 专利公告日期
  - `patentType`: 专利类型
- `total`: 专利总数

### 3. patent_bigdata_patent_stats
**功能**: 企业专利统计分析

根据提供的企业信息查询企业的专利情况，包括专利状态分布、专利申请与授权趋势、以及按专利类型分布的专利数量等。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 企业名称/注册号/统一社会信用代码/企业id
- `keywordType` (可选): 主体类型 - name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码

**返回值**:
- `patentDivAppLegalStat`: 专利状态分布
  - `patentCount`: 专利数量
  - `patentDivAppLegal`: 专利状态名称
- `patentTypeAppTimeStat`: 专利申请趋势
  - `appearanceDesignPatentCount`: 外观设计专利数量
  - `inventionLicPatentCount`: 发明授权专利数量
  - `inventionAppPatentCount`: 发明申请专利数量
  - `year`: 年份
- `patentTypePubTimeStat`: 专利授权趋势
  - `utilityModelPatentCount`: 实用新型专利数量
  - `appearanceDesignPatentCount`: 外观设计专利数量
  - `year`: 年份
- `patentTypeStat`: 专利类型分布

## 使用场景

1. **专利代理机构**: 获取竞争对手的专利布局情况
2. **研发人员**: 查找特定领域的已有专利以规避侵权
3. **企业技术创新**: 进行专利情报分析，判断市场竞争态势
4. **投资分析**: 评估企业创新能力和技术储备
5. **法律诉讼**: 专利侵权风险评估
6. **科技项目评估**: 了解技术领域专利分布

## 使用注意事项

1. **企业全称要求**: 在调用需要企业全称的接口时，如果没有企业全称则先调取patent_bigdata_fuzzy_search接口获取企业全称
2. **分页限制**: 一页最多获取50条数据
3. **专利类型**: 支持按发明申请、实用新型、发明授权、外观设计等类型筛选
4. **搜索方式**: 支持按专利名称、申请号、申请人、代理机构等多种方式搜索
5. **统计分析**: 提供专利状态分布、申请趋势、授权趋势等多维度统计分析

## 使用提问示例

### patent_bigdata_fuzzy_search (企业关键词模糊搜索)
1. 帮我查找包含"华为"关键词的企业信息
2. 搜索与"小米"相关的企业列表
3. 查询名称中包含"大疆"的公司

### patent_bigdata_patent_search (专利信息搜索)
1. 查询华为技术有限公司申请的所有专利
2. 搜索关键词为"5G通信"的专利信息
3. 查找申请号为"CN202012345678"的专利详情

### patent_bigdata_patent_stats (企业专利统计分析)
1. 分析华为近几年的专利申请趋势
2. 查询腾讯科技的专利类型分布统计
3. 阿里巴巴集团的专利授权趋势如何？ 