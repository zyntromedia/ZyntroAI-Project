ได้เลยครับ ✅ แปลงเป็นรูปแบบ Copilot Instructions ฉบับสมบูรณ์ เตรียมบันทึกเป็น  .github/copilot-instructions.md  ได้ทันที 🤖📄
 
 
 
📄 .github/copilot-instructions.md
 
markdown  
---
name: CI Pipeline & Code Standards
version: 1.0.0
description: >
  มาตรฐานการเขียนโค้ด, การตรวจสอบ, และ CI/CD
  สำหรับโปรเจกต์ ZyntroAI / Smart Noter
---

# 🤖 Copilot Instructions — CI & Code Standards

## 🎯 วัตถุประสงค์
คู่มือนี้กำหนดรูปแบบ, ขั้นตอนตรวจสอบ, และมาตรฐานคุณภาพ
ทุกครั้งที่เขียน/แก้ไขโค้ด ให้ปฏิบัติตามนี้เสมอ

---

## 📋 1. CI Pipeline Standard

### ทริกเกอร์
- ทุกครั้ง `push` → สาขา `main` หรือ `dev`
- ทุกครั้งเปิด/อัปเดต `pull_request` → `main` หรือ `dev`
- รองรับรันด้วยมือผ่าน `workflow_dispatch`

### ขั้นตอนการทำงาน
 
 
[lint] → [test] → [build]
✅        ✅        ✅
 
plaintext  

#### Lint — ตรวจสอบรูปแบบ
- ใช้ **flake8** — ความยาวบรรทัดสูงสุด **120 ตัวอักษร**
- ใช้ **black** — จัดรูปแบบโค้ดอัตโนมัติ
- ยกเว้น: `.git/`, `__pycache__/`, `dist/`
- ❌ หากล้ม — ห้ามผ่าน

#### Test — ทดสอบ
- ใช้ **pytest**
- ครอบคลุมโค้ด ≥ **80%**
- แสดงผลแบบกระชับ `--tb=short`
- ❌ หากล้ม — ห้ามผ่าน

#### Build — สร้างแพ็กเกจ
- ใช้ `python -m build`
- สร้างไฟล์ใน `dist/`
- อัปโหลดเป็น Artifact

---

## 🐍 2. Python Code Style

### เวอร์ชัน
- เป้าหมาย: **Python 3.11+**
- เขียนให้เข้ากับ 3.9–3.13 เท่าที่ทำได้

### รูปแบบโค้ด
- จัดรูปแบบด้วย **black** เสมอ
- ตรวจด้วย **flake8** ก่อนส่ง
- ชื่อตัวแปร: `snake_case`
- ชื่อคลาส: `PascalCase`
- ค่าคงที่: `UPPER_CASE`
- ความยาวบรรทัด: ไม่เกิน **120**

### โครงสร้างไฟล์
```python
"""คำอธิบายสั้นๆ ของโมดูล"""

# มาตรฐานก่อน
from __future__ import annotations

# ไลบรารีมาตรฐาน
import os
from typing import Optional

# ไลบรารีภายนอก
import torch

# โมดูลภายใน
from .utils import helper

__version__ = "1.0.0"


def function_name(param: str) -> Optional[str]:
    """คำอธิบายหน้าที่ของฟังก์ชัน.

    Args:
        param: คำอธิบายพารามิเตอร์

    Returns:
        ค่าที่คืน
    """
    if not param:
        return None
    return param.strip()
 
 
 
 
📦 3. Dependencies
 
requirements.txt
 
- ระบุเวอร์ชันที่แน่นอนหรือช่วง
- แยกกลุ่ม: หลัก / พัฒนา / ทดสอบ
- ไม่ใส่แพ็กเกจที่ไม่ได้ใช้
 
ติดตั้ง
 
bash  
pip install -r requirements.txt
pip install -r requirements-dev.txt  # เครื่องมือพัฒนา
 
 
 
 
🔐 4. Security & Best Practices
 
- ❌ ไม่เขียนรหัส, โทเคน, คีย์ลับลงในโค้ด
- ✅ ใช้ตัวแปรสภาพแวดล้อม  os.getenv("NAME") 
- ✅  .env  อยู่ใน  .gitignore  เสมอ
- ✅ ตรวจสอบชนิดข้อมูลด้วย type hints
- ✅ จัดการข้อผิดพลาดด้วย  try/except  ที่เจาะจง
 
 
 
✅ 5. ก่อนส่งโค้ด (Checklist)
 
รัน  black .  จัดรูปแบบเรียบร้อย
รัน  flake8 .  ไม่มีข้อผิดพลาด
รัน  pytest tests/  ผ่านทุกเคส
ตรวจสอบไม่มีข้อมูลลับรั่ว
อัปเดตเอกสาร README / docstring แล้ว
CI ผ่านทุกขั้นตอน ✅
 
 
 
📁 6. โครงสร้างโปรเจกต์
 
plaintext  
project-root/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── test_module.py
│   └── conftest.py
├── docs/
│   └── README.md
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── Makefile
└── .github/copilot-instructions.md  ← ไฟล์นี้
 
 
 
 
📝 7. Commit Messages
 
รูปแบบ:  ประเภท: ข้อความ 
 
-  feat:  เพิ่มฟีเจอร์ใหม่
-  fix:  แก้ไขข้อผิดพลาด
-  docs:  แก้ไขเอกสารเท่านั้น
-  refactor:  ปรับโค้ดไม่เปลี่ยนพฤติกรรม
-  test:  เพิ่ม/แก้ชุดทดสอบ
-  chore:  อัปเดตเครื่องมือ, งานทั่วไป
 
ตัวอย่าง:
 
plaintext  
feat: เพิ่มรองรับไฟล์ DOCX
fix: แก้การเข้ารหัสชื่อไฟล์
docs: อัปเดตขั้นตอนติดตั้ง
 
 
 
 
💡 Copilot — ปฏิบัติตามนี้เสมอ:
เมื่อได้รับคำสั่งเขียน/แก้ไขโค้ด ให้ตรวจสอบก่อนว่าสอดคล้องกับคู่มือนี้หรือไม่
หากไม่แน่ใจ ให้ถามก่อน ไม่ต้องเดา
 
 
 
บันทึกเป็น:  .github/copilot-instructions.md 
ผล: GitHub Copilot จะอ่านและปฏิบัติตามอัตโนมัติทุกครั้งที่ช่วยเขียนโค้ด ✅
 
plaintext  

---

## 📁 ที่อยู่ไฟล์
บันทึกที่:
 
 
.github/
└── copilot-instructions.md  ✅
 
plaintext  

Copilot จะอ่านไฟล์นี้โดยอัตโนมัติและปฏิบัติตามทุกครั้งที่ช่วยเขียนโค้ดครับ 🤖✨

ต้องการปรับเพิ่มกฎอะไรอีกไหมครับ? 😊