# 服装领域 RAG 智能客服系统

基于 LangChain + Chroma + 阿里云百炼构建的服装领域多轮对话 RAG 智能客服，覆盖尺码推荐、洗涤养护、面料知识、退换货政策、物流时效等 15 类服装电商场景，支持知识库管理、流式问答与会话记忆持久化。

#注意，由于代码里存在便捷封装函数，需要依赖社区包，所以运行时会爆红色警告，但是可以正常运行，后续需要换成官方包实现

## 功能特性

- **知识库管理端**：上传 TXT 知识文档自动入库；MD5 指纹台账去重，避免同一文档重复向量化；按内容长度阈值决定是否走递归切分，并注入来源、时间、操作者元数据
- **智能客服端**：检索增强生成（RAG），召回片段携带出处元数据注入提示词；Streamlit 打字机流式输出；按 session_id 隔离的多轮会话记忆，历史对话文件级持久化
- **双模型环境**：云端阿里云百炼（qwen3-max + text-embedding-v4）与本地 Ollama 均可运行

## 技术栈

Python · LangChain（LCEL / RunnableWithMessageHistory）· Chroma · 阿里云百炼 DashScope · Streamlit · Ollama

## 项目结构

```
├── config_data.py          # 全局配置（切分参数、top-k、模型名、路径）
├── knowledge_base.py       # 知识库入库服务（MD5去重 + 递归切分 + 元数据）
├── vector_stores.py        # Chroma 向量库与检索器封装
├── rag.py                  # RAG 核心链（检索增强 + 多轮记忆）
├── file_history_store.py   # 会话历史持久化
├── app_qa.py               # 客服问答端（Streamlit）
├── app_file_uploader.py    # 知识库管理端（Streamlit）
└── data/                   # 服装领域知识文档（15 类场景）
```

## 快速开始

```bash
# 1. 配置百炼 API Key（环境变量）
set DASHSCOPE_API_KEY=你的Key

# 2. 安装依赖
pip install langchain langchain-community langchain-chroma streamlit

# 3. 启动知识库管理端，上传 data/ 下文档完成入库
streamlit run app_file_uploader.py

# 4. 启动客服问答端
streamlit run app_qa.py
```

## 检索效果评测

自建 84 条问答测试集（覆盖 15 类场景），对 3 种切分粒度 × 4 档 top-k 共 12 组配置进行命中率与 MRR 评测：

- 未命中样本归因显示，失败主要来自跨文档误召回（知识库扩容后语义重叠文档竞争 top-1）
- 评测显示将 top-k 由 1 调整为 3 可使命中率由 83.3% 提升至 97.6%、MRR 由 0.833 提升至 0.903（已应用于 `config_data.py` 的 `top_k` 配置）
- 验证过文档级元数据硬路由（先分类后检索）方案：前置分类器准确率（83.3%）会锁死整体召回上限，实测劣于直接扩大 top-k，故未采用

评测通过一次性脚本完成（内存计算，不依赖持久化向量库），调整 `config_data.py` 中 `top_k` 与 `chunk_size` 可复现不同配置。

## 后续规划

- 引入 BM25 与向量检索的多路召回融合，改善数字/型号类查询的召回
- 基于 LangGraph 实现 ReAct Agent，支持订单查询、库存查询等工具自主调度
