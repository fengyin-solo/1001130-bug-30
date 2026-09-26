"""内存数据仓库：给每个业务模块准备一份可筛选、可流转的示例数据。

真实项目里这里会换成数据库访问层；当前实现只依赖标准库，保证克隆下来就能起。
"""
from __future__ import annotations

from typing import Any

from app.seed import SEED_ROWS

# 模块中文名与展示顺序：和前端导航、各模块页面标题保持一致，
# 概览清单按这个顺序输出，保证看板与模块页面说的是同一批模块。
MODULE_LABELS: dict[str, str] = {
    "berth": "泊位计划",
    "vessel": "船舶档案",
    "voyage": "航次管理",
    "crane": "岸桥作业",
    "loading": "装卸任务",
    "yard": "堆场管理",
    "container": "集装箱档案",
    "yardstore": "堆存记录",
    "gate": "闸口通行",
    "truck": "集卡调度",
    "tally": "理货作业",
    "damage": "残损登记",
    "manifest": "单证处理",
    "storage": "堆存计费",
    "pilot": "引航拖轮",
    "safety": "安全监督",
    "customer": "货主档案",
    "settle": "作业结算",
}


class Store:
    def __init__(self) -> None:
        self._tables: dict[str, list[dict[str, Any]]] = {
            name: [dict(row) for row in rows] for name, rows in SEED_ROWS.items()
        }

    def module_names(self) -> list[str]:
        return sorted(self._tables)

    def rows(self, module: str) -> list[dict[str, Any]]:
        return self._tables.setdefault(module, [])

    def find(self, module: str, entry_id: int) -> dict[str, Any] | None:
        for row in self.rows(module):
            if int(row.get("id", 0)) == entry_id:
                return row
        return None

    def overview(self) -> dict[str, object]:
        """按同一份业务数据汇总看板口径。

        待处理只算仍需跟进且未标记异常的记录：已处理（pending=False）不再计入，
        异常记录单独进异常量，不从待处理里扣、也不重复显示成待处理。
        """
        modules: list[dict[str, object]] = []
        for key, label in MODULE_LABELS.items():
            rows = self.rows(key)
            modules.append({
                "name": label,
                "created": len(rows),
                "pending": sum(1 for row in rows if row.get("pending") and not row.get("abnormal")),
                "abnormal": sum(1 for row in rows if row.get("abnormal")),
            })
        cards = [
            {"label": "业务模块", "value": len(modules)},
            {"label": "今日新增", "value": sum(int(item["created"]) for item in modules)},
            {"label": "待处理", "value": sum(int(item["pending"]) for item in modules)},
            {"label": "异常量", "value": sum(int(item["abnormal"]) for item in modules)},
        ]
        return {"cards": cards, "modules": modules}


store = Store()
