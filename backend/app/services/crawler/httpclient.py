"""统一 HTTP 客户端：优先 httpx，失败（403/网络阻断等）回退到系统 curl。

背景：部分数据源（如 Wikimedia）对数据中心出口 IP 返回 403 机器人策略，
但系统 curl 在同网络下可达。为兼顾「沙箱可演示」与「用户本机可运行」，
这里做 httpx -> curl 的优雅回退。
"""
from __future__ import annotations

import asyncio
import json
import shutil

import httpx

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


async def fetch(url: str, *, as_json: bool = False, timeout: int = 15, headers: dict | None = None):
    h = {"User-Agent": BROWSER_UA}
    if headers:
        h.update(headers)
    try:
        async with httpx.AsyncClient(timeout=timeout, headers=h, follow_redirects=True) as c:
            r = await c.get(url)
            r.raise_for_status()
            return r.json() if as_json else r.text
    except Exception:
        pass

    # 回退：系统 curl（Windows 10+/Linux/macOS 均自带）
    if shutil.which("curl"):
        try:
            proc = await asyncio.create_subprocess_exec(
                "curl", "-sL", "--max-time", str(timeout), "-A", BROWSER_UA, url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out, _ = await proc.communicate()
            text = out.decode("utf-8", "replace")
            if as_json:
                return json.loads(text)
            return text
        except Exception:
            return None
    return None
