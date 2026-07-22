"""启动入口：uvicorn 运行 FastAPI。dev 用 reload；生产可去掉 reload。"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
