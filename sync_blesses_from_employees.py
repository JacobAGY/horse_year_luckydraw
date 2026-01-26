#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 assets/images/employees/ 下的实际文件，更新 assets/blesses.json：
- avatar 改为 employees 下真实存在的路径（含正确扩展名 .png/.jpeg 等）
- 仅保留在 employees 中有文件的条目
- 顺序与员工文件名排序一致，name/blessing 沿用原 blesses 中能匹配到的内容
"""

import os
import json

EMPLOYEES_DIR = "assets/images/employees"
BLESSES_JSON = "assets/blesses.json"

def base_to_id(base):
    return base.replace("_", "-")

def base_to_name(base):
    """frank_liu -> Frank Liu, sandra_h_y_chen -> Sandra H Y Chen"""
    parts = base.split("_")
    return " ".join(p.capitalize() for p in parts)

def main():
    # 当前 blesses：id -> { id, name, avatar, blessing }
    with open(BLESSES_JSON, "r", encoding="utf-8") as f:
        blesses = json.load(f)
    by_id = {b["id"]: b for b in blesses}

    # employees 下所有图片
    allowed = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    files = [f for f in os.listdir(EMPLOYEES_DIR) if f.lower().endswith(allowed)]

    out = []
    for fn in sorted(files):
        base, ext = os.path.splitext(fn)
        rel = f"assets/images/employees/{fn}"
        id_ = base_to_id(base)
        old = by_id.get(id_)
        if old:
            entry = {
                "id": old["id"],
                "name": old["name"],
                "avatar": rel,
                "blessing": old.get("blessing", ""),
            }
        else:
            entry = {
                "id": id_,
                "name": base_to_name(base),
                "avatar": rel,
                "blessing": "",
            }
        out.append(entry)

    with open(BLESSES_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"已根据 employees 目录更新 blesses.json，共 {len(out)} 条")

if __name__ == "__main__":
    main()
