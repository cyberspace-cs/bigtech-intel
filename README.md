# 大厂情报站 · AI 大模型厂求职参谋

面向**实习 / 校招 / 社招**的大厂信息资源站：检索大厂（字节 Seed / 腾讯混元 / 智谱 GLM / Kimi / DeepSeek 等 20 家）的
**JD 画像、团队背景图谱、简历策略、招聘入口**，并细化每家的**近期进展（发布的大模型 / 产品）**与**目前的技术架构**，
方便面试前快速摸清业务线、做简历定制。

> 数据来源：用户原始投递策略 + 公开资料摘编（截至 2026-07），面试前请以官方最新 JD 复核。

## 技术架构

- **后端**：Python · FastAPI · SQLAlchemy · SQLite（零外部依赖，本地即跑）
  - `backend/app/routers/`：companies（搜索/筛选/详情）、teams（派系图谱）、resume、recruit、crawl
  - `backend/app/services/crawler/`：可扩展爬虫框架（BaseCrawler + wikipedia/baidu_baike/official_site 适配器 + 统一 http 客户端）
- **前端**：Vue 3 · Vite（政务蓝白 / 科技感主题），`/api` 代理到后端
- 后端 `main.py` 启动自动建表 + 灌种子数据；生产模式下挂载 `frontend/dist` 静态产物

## 本地运行

### 1. 后端（默认 8031 端口）

```bash
cd backend
pip install -r requirements.txt
python -m app.seed            # 建表 + 灌种子数据（幂等，可重复执行）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8031
```

### 2. 前端（Vite 开发服务器，默认 5173 端口）

```bash
cd frontend
npm install
npm run dev                   # 访问 http://localhost:5173/
```

> 生产部署：先 `npm run build` 生成 `frontend/dist`，后端会自动托管该目录。

## 目录结构

```
bigtech-intel/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── routers/        # 各业务路由
│   │   ├── services/crawler/  # 可扩展爬虫框架
│   │   ├── models.py / schemas.py / database.py
│   │   ├── seed.py         # 幂等灌库（含 SQLite ALTER 迁移）
│   │   └── seed_data.py    # 20 家公司画像 / 图谱 / 简历策略 / 招聘表
│   ├── crawl_cli.py        # 前台批量爬虫
│   └── requirements.txt
├── frontend/               # Vue3 + Vite 前端
├── index.html / styles.css / data.js / app.js   # 早期静态版（可独立打开）
└── README.md
```

## 补充说明

- 爬虫：`python crawl_cli.py wikipedia` 可批量补抓公开资料（依赖网络；沙箱/企业网环境可能受限）。
- 数据库 `backend/data/app.db` 由 `seed` 自动生成，**不入库**；如需重置删除该文件后重跑 `seed` 即可。
