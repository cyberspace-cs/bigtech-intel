"""前台批量爬虫 CLI：用同一套适配器把公开资料灌入数据库。

用法：
    python crawl_cli.py                 # 默认 Wikipedia，遍历全部公司
    python crawl_cli.py baidu_baike     # 指定适配器
    python crawl_cli.py wikipedia --limit 5

说明：本脚本在前台运行（网络出口与交互式 shell 一致，可正常抓取）；
应用内 /api/crawl/trigger 同样可用，取决于部署环境的网络策略。
"""
import asyncio
import sys

from app.database import SessionLocal
from app.models import Company
from app.services.crawler.manager import crawl_query


async def main(adapter: str, limit: int):
    db = SessionLocal()
    companies = db.query(Company).order_by(Company.tier, Company.name).all()
    db.close()

    if limit:
        companies = companies[:limit]

    ok = fail = 0
    for c in companies:
        print(f"[抓取] {c.name} ({adapter}) ...", end=" ", flush=True)
        logs = await crawl_query(
            c.name, adapter=adapter, company_id=c.id, trigger="cli", link_to_company=True
        )
        best = None
        for l in logs:
            if l.get("status") == "success":
                ok += 1
                best = l
                break
            else:
                fail += 1
        if best:
            print("OK ->", best.get("message", "")[:70])
        else:
            print("失败")
        await asyncio.sleep(0.4)  # 礼貌限速
    print(f"\n完成：成功 {ok} / 失败 {fail}（共 {len(companies)} 家）")


if __name__ == "__main__":
    adp = sys.argv[1] if len(sys.argv) > 1 else "wikipedia"
    lim = 0
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        lim = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 0
    asyncio.run(main(adp, lim))
