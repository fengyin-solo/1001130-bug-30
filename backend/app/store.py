"""内存数据仓库：给每个业务模块准备一份可筛选、可流转的示例数据。

真实项目里这里会换成数据库访问层；当前实现只依赖标准库，保证克隆下来就能起。
"""
from __future__ import annotations

from typing import Any

from app.seed import SEED_ROWS

# 模块键对应的中文名：概览清单与前端导航、各模块页面标题用同一份叫法。
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


def is_pending_status(status: object) -> bool:
    """待处理口径：状态以「待」开头才算待处理。

    已流转的状态（已编排、已放行、作业中……）一律不再计入待处理；
    异常量按 abnormal 标志单独统计，不从待处理里扣，也不重复算进待处理。
    """
    return str(status or "").startswith("待")


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

    def module_summary(self, module: str) -> dict[str, object]:
        """单个模块的汇总：新增、待处理、异常量都按当前记录实时重算。"""
        rows = self.rows(module)
        return {
            "key": module,
            "name": MODULE_LABELS.get(module, module),
            "created": len(rows),
            "pending": sum(1 for row in rows if is_pending_status(row.get("status"))),
            "abnormal": sum(1 for row in rows if row.get("abnormal")),
        }

    def overview(self) -> dict[str, object]:
        """运营概览：卡片由各模块汇总行求和得出，保证卡片与清单是同一份数。"""
        modules = [self.module_summary(name) for name in self.module_names()]
        cards = [
            {"label": "业务模块", "value": len(modules)},
            {"label": "今日新增", "value": sum(int(item["created"]) for item in modules)},
            {"label": "待处理", "value": sum(int(item["pending"]) for item in modules)},
            {"label": "异常量", "value": sum(int(item["abnormal"]) for item in modules)},
        ]
        return {"cards": cards, "modules": modules}


store = Store()
