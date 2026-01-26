#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 employees 目录中的图片文件转换为 .png，并更新 blesses.json 中的路径
使用 macOS 的 sips 命令进行转换
"""

import os
import json
import subprocess

EMPLOYEES_DIR = "assets/images/employees"
BLESSES_JSON = "assets/blesses.json"

def convert_jpg_to_png():
    """将所有 .jpg/.jpeg 文件转换为 .png 并更新 JSON"""
    
    # 读取 blesses.json
    with open(BLESSES_JSON, 'r', encoding='utf-8') as f:
        blesses = json.load(f)
    
    # 创建文件名映射：旧名 -> 新名
    name_mapping = {}
    
    # 遍历 employees 目录
    if os.path.exists(EMPLOYEES_DIR):
        for filename in os.listdir(EMPLOYEES_DIR):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                old_path = os.path.join(EMPLOYEES_DIR, filename)
                # 生成新的 .png 文件名
                base_name = os.path.splitext(filename)[0]
                new_filename = base_name + '.png'
                new_path = os.path.join(EMPLOYEES_DIR, new_filename)
                
                # 使用 sips 转换图片格式
                try:
                    result = subprocess.run(
                        ['sips', '-s', 'format', 'png', old_path, '--out', new_path],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        # 删除旧文件
                        os.remove(old_path)
                        
                        # 记录映射关系
                        old_relative = f"assets/images/employees/{filename}"
                        new_relative = f"assets/images/employees/{new_filename}"
                        name_mapping[old_relative] = new_relative
                        
                        print(f"转换: {filename} -> {new_filename}")
                    else:
                        print(f"转换失败 {filename}: {result.stderr}")
                except Exception as e:
                    print(f"转换失败 {filename}: {e}")
    
    # 更新 blesses.json 中的路径
    updated = 0
    for bless in blesses:
        avatar = bless.get('avatar', '')
        if avatar in name_mapping:
            bless['avatar'] = name_mapping[avatar]
            updated += 1
        elif avatar.endswith('.jpg') or avatar.endswith('.jpeg'):
            # 如果路径不在映射中，直接替换扩展名
            new_avatar = os.path.splitext(avatar)[0] + '.png'
            bless['avatar'] = new_avatar
            updated += 1
    
    # 保存更新后的 blesses.json
    if updated > 0:
        with open(BLESSES_JSON, 'w', encoding='utf-8') as f:
            json.dump(blesses, f, ensure_ascii=False, indent=2)
        print(f"\n已更新 {updated} 条记录的头像路径为 .png")
    else:
        print("\n没有需要更新的记录")

if __name__ == "__main__":
    convert_jpg_to_png()
