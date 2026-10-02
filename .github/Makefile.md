# ==========================================
# SMART NOTER — Makefile
# ==========================================

# ===== การตั้งค่า =====
PYTHON = python3
PIP = pip
SRC = smart_noter.py
PKG_NAME = smart-noter

# ===== ค่าเริ่มต้น =====
.DEFAULT_GOAL := help

# ===== แสดงรายการคำสั่ง =====
help:
	@echo "=========================================="
	@echo "🎙️  SMART NOTER — คำสั่งที่ใช้ได้"
	@echo "=========================================="
	@echo ""
	@echo "ติดตั้ง:"
	@echo "  make install       ติดตั้งแพ็กเกจทั้งหมด"
	@echo "  make install-dev   ติดตั้งพร้อมเครื่องมือพัฒนา"
	@echo "  make editable      ติดตั้งแบบแก้ไขได้"
	@echo ""
	@echo "ใช้งาน:"
	@echo "  make run           รันโปรแกรม"
	@echo "  make run FILE=...  รันพร้อมระบุไฟล์ทันที"
	@echo ""
	@echo "ตรวจสอบ & ทดสอบ:"
	@echo "  make lint          ตรวจสอบรูปแบบโค้ด"
	@echo "  make format        จัดรูปแบบโค้ดอัตโนมัติ"
	@echo "  make test          รันชุดทดสอบ"
	@echo ""
	@echo "จัดการ:"
	@echo "  make clean         ลบไฟล์ขยะ"
	@echo "  make build         สร้างแพ็กเกจสำหรับแจกจ่าย"
	@echo "  make uninstall     ถอนการติดตั้ง"
	@echo ""

# ===== ติดตั้ง =====
install:
	@echo "📦 กำลังติดตั้งแพ็กเกจ..."
	$(PIP) install -r requirements.txt
	@echo "✅ ติดตั้งเสร็จสิ้น"

install-dev:
	@echo "🛠️  กำลังติดตั้งพร้อมเครื่องมือพัฒนา..."
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 pytest
	@echo "✅ ติดตั้งเสร็จสิ้น"

editable:
	@echo "🔧 กำลังติดตั้งแบบแก้ไขได้..."
	$(PIP) install -e .
	@echo "✅ ติดตั้งเสร็จสิ้น — ใช้คำสั่ง 'smart-noter' ได้เลย"

# ===== ใช้งาน =====
run:
	@echo "🎙️  กำลังเริ่มทำงาน..."
	$(PYTHON) $(SRC) $(FILE)

# ===== ตรวจสอบ & จัดรูปแบบ =====
lint:
	@echo "🔍 ตรวจสอบรูปแบบโค้ด..."
	-flake8 $(SRC) --max-line-length=120
	@echo "✅ ตรวจสอบเสร็จสิ้น"

format:
	@echo "✨ จัดรูปแบบโค้ด..."
	-black $(SRC)
	@echo "✅ จัดรูปแบบเสร็จสิ้น"

test:
	@echo "🧪 รันชุดทดสอบ..."
	-$(PYTHON) -m pytest tests/ -v
	@echo "✅ ทดสอบเสร็จสิ้น"

# ===== จัดการไฟล์ =====
clean:
	@echo "🧹 กำลังลบไฟล์ขยะ..."
	-find . -name "__pycache__" -type d -exec rm -rf {} +
	-find . -name "*.pyc" -delete
	-find . -name "*.pyo" -delete
	-find . -name "*.pyd" -delete
	-rm -rf .pytest_cache
	-rm -rf dist build *.egg-info
	-rm -f ผลลัพธ์.txt สรุป_*.txt
	@echo "✅ ทำความสะอาดเสร็จสิ้น"

# ===== สร้างแพ็กเกจแจกจ่าย =====
build: clean
	@echo "📦 กำลังสร้างแพ็กเกจ..."
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build
	@echo "✅ สร้างเสร็จ — ดูที่โฟลเดอร์ dist/"

# ===== ถอนการติดตั้ง =====
uninstall:
	@echo "🗑️  กำลังถอนการติดตั้ง..."
	-$(PIP) uninstall -y $(PKG_NAME)
	@echo "✅ ถอนเสร็จสิ้น"

# ===== ป้องกันชื่อซ้ำกับไฟล์จริง =====
.PHONY: help install install-dev editable run lint format test clean build uninstall
