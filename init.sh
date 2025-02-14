#!/bin/bash

# 检查 Miniforge 是否已安装
if [ -d "$HOME/miniforge3" ]; then
    echo "Miniforge 已经安装在 $HOME/miniforge3"
else
    echo "Miniforge 尚未安装，正在安装..."

    # 下载 Miniforge 安装脚本
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

    # 赋予执行权限
    chmod +x Miniforge3-$(uname)-$(uname -m).sh

    # 运行安装脚本
    bash Miniforge3-$(uname)-$(uname -m).sh -b -p $HOME/miniforge3

    # 清理安装脚本
    rm Miniforge3-$(uname)-$(uname -m).sh

    echo "Miniforge 安装完成，路径: $HOME/miniforge3"
fi

# 初始化 conda（如果尚未初始化）
if [ ! -f "$HOME/.conda" ]; then
    $HOME/miniforge3/bin/conda init
    echo ".conda初始化完成" > "$HOME/.conda初始化完成"
    echo "请重新启动终端或运行 'source ~/.bashrc'（或 'source ~/.zshrc' 如果使用 zsh）以激活 conda。"
else
    echo "Conda 已经初始化。"
fi

# 检查是否存在 env.yaml 文件
if [ ! -f "env.yaml" ]; then
    echo "当前目录下未找到 env.yaml 文件，请确保 env.yaml 存在以创建 conda 环境。"
    exit 1
fi

# 获取环境名称（假设从 env.yaml 中第一行的 name 字段获取）
ENV_NAME=$(grep -oP 'name:\s*\K\w+' env.yaml)

if [ -z "$ENV_NAME" ]; then
    echo "无法从 env.yaml 中解析出环境名称。"
    exit 1
fi

# 检查环境是否已存在，如果存在则删除
if [ -d "$HOME/miniforge3/envs/$ENV_NAME" ]; then
    echo "环境 $ENV_NAME 已存在，正在删除..."
    $HOME/miniforge3/bin/conda env remove -n $ENV_NAME
fi

# 创建新的 conda 环境
echo "正在根据 env.yaml 创建环境 $ENV_NAME..."
$HOME/miniforge3/bin/conda env create -f env.yaml

# 激活环境
echo "激活环境 $ENV_NAME..."
source $HOME/miniforge3/bin/activate $ENV_NAME

echo "环境 $ENV_NAME 创建并激活成功。"