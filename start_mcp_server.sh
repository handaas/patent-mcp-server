#!/bin/bash

# HandaaS分类MCP服务器启动脚本

echo "启动HandaaS分类MCP服务器..."

# 检查虚拟环境
if [ ! -d "mcp_env" ]; then
    echo "错误: 虚拟环境不存在，请先运行 python -m venv mcp_env"
    exit 1
fi

# 激活虚拟环境
source mcp_env/bin/activate

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "警告: .env文件不存在，请确保已配置API认证信息"
    echo "需要配置以下环境变量:"
    echo "  INTEGRATOR_ID=你的对接器ID"
    echo "  SECRET_ID=你的密钥ID"
    echo "  SECRET_KEY=你的密钥"
fi

# 安装依赖
echo "检查Python依赖..."
pip install -q python-dotenv requests mcp

# 启动服务器
echo "启动企业MCP服务器..."
cd server
python mcp_server.py

echo "企业MCP服务器已停止" 