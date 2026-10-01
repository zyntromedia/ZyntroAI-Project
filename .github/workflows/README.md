ได้เลยครับ! นี่คือคู่มือ  .github/workflows/  แบบครบถ้วน เข้าใจง่าย พร้อมตัวอย่างใช้งานจริง 🚀
 
 
 
📂 โครงสร้างพื้นฐาน
 
plaintext  
your-repo/
├── .github/
│   ├── workflows/          # ← เก็บไฟล์นี้ที่นี่!
│   │   ├── ci.yml          # ตรวจสอบโค้ด → ทดสอบ
│   │   ├── deploy.yml      # ปรับใช้งานจริง
│   │   └── ensure-codeowners.yml  # สร้าง CODEOWNERS อัตโนมัติ
│   ├── CODEOWNERS
│   └── dependabot.yml
└── ...
 
 
✅ ทุกไฟล์ต้องลงที่  .github/workflows/*.yml  เท่านั้น
 
 
 
🧩 ส่วนประกอบหลัก (รู้ไว้ใช่ว่า)
 
ส่วน ความหมาย ตัวอย่าง 
 name  ชื่อแสดงในหน้า Actions  name: CI Pipeline  
 on  ทริกเกอร์ — เมื่อไหร่จะทำงาน  push ,  pull_request ,  schedule ,  workflow_dispatch  
 jobs  กลุ่มงาน — ทำอะไรบ้าง ทดสอบ → สร้าง → ปรับใช้ 
 runs-on  เครื่องที่รัน  ubuntu-latest ,  macos-latest ,  windows-latest  
 steps  ขั้นตอนย่อย เช็คเอาท์โค้ด → ติดตั้ง → รันคำสั่ง 
 uses  เรียกใช้ Action สำเร็จรูป  actions/checkout@v4  
 run  รันคำสั่งเชลล์  npm test  
 
 
 
🔥 ตัวอย่างที่ 1: CI พื้นฐาน (ci.yml)
 
yaml  
name: CI — Build & Test

# ทริกเกอร์: ดันโค้ด หรือเปิด PR เข้า main
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# สิทธิ์ขั้นต่ำ (แนะนำเสมอ)
permissions:
  contents: read

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'  # ✅ แคช ลดเวลารันรอบต่อไป

      - name: Install dependencies
        run: npm ci

      - name: Lint code
        run: npm run lint

      - name: Run tests
        run: npm test
 
 
 
 
🔥 ตัวอย่างที่ 2: ปรับใช้ (deploy.yml)
 
yaml  
name: Deploy to Production

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: 'npm' }
      - run: npm ci
      - run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with: { path: './dist' }

  deploy:
    needs: build  # ✅ รอ build เสร็จก่อน
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
 
 
 
 
🔥 ตัวอย่างที่ 3: สร้าง CODEOWNERS อัตโนมัติ (ที่คุณใช้อยู่)
 
yaml  
name: Ensure CODEOWNERS Exists

on:
  push:
    branches: [main]
  workflow_dispatch:  # ✅ กดรันด้วยมือได้

permissions:
  contents: write
  pull-requests: write

jobs:
  check-and-create:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create CODEOWNERS if missing
        if: |
          !(exists('CODEOWNERS') || exists('.github/CODEOWNERS'))
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git checkout -B automation/add-codeowners
          
          mkdir -p .github
          cat > .github/CODEOWNERS <<'EOF'
# CODEOWNERS
/scripts/       @MY-ORG/team-backend
/tests/          @MY-ORG/team-qa
/.github/       @MY-ORG/devops
*               @MY-ORG/maintainers
EOF

          git add .github/CODEOWNERS
          git commit -m "chore: add CODEOWNERS template" || exit 0
          git push --set-upstream origin automation/add-codeowners --force-with-lease

      - name: Open PR
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          title: "chore: add CODEOWNERS template"
          body: "Auto-generated file — please review & merge."
          head: automation/add-codeowners
          base: main
          delete-branch: true
 
 
 
 
⚙️ ทริกเกอร์ยอดนิยม ( on: )
 
รูปแบบ ทำงานเมื่อ 
 on: push  ทุกครั้งที่ดันโค้ด 
 on: pull_request  เปิด/อัปเดต PR 
 on: schedule: [{cron: '0 8 * * 1'}]  ทุกจันทร์ 8 โมงเช้า 
 on: workflow_dispatch  กดปุ่มรันด้วยมือจากหน้าเว็บ 
 on: release  เมื่อสร้าง Release 
 
⏰ Cron:  นาที ชั่วโมง วัน เดือน วันสัปดาห์  — เวลาเป็น UTC
 
 
 
✅ แนวทางปฏิบัติที่ดี
 
1. แยกไฟล์ตามหน้าที่ — ไม่เขียนทุกอย่างรวมกันไฟล์เดียว
-  ci.yml  = ตรวจสอบ → ทดสอบ
-  deploy.yml  = ปรับใช้
-  lint.yml  = ตรวจสอบรูปแบบโค้ด
2. ใช้  permissions:  จำกัดสิทธิ์ — ให้น้อยที่สุดเสมอ
yaml  
permissions:
  contents: read   # อ่านได้อย่างเดียว พอแล้วส่วนใหญ่
 
3. Pin เวอร์ชันด้วย commit hash ป้องกันการเปลี่ยนแปลงไม่คาดฝัน
yaml  
uses: actions/checkout@a5ac7e51b41d4c924da31875e65281d90459d49d # v4.1.0
 
4. ใช้แคช ลดเวลารันซ้ำๆ
yaml  
with: { cache: 'npm' }  # ใน setup-node
 
5. ตั้งชื่อไฟล์ชัดเจน —  ci.yml ,  deploy-prod.yml ,  codeowners-sync.yml 
 
 
 
📌 ขั้นตอนเริ่มใช้งานจริง
 
1. สร้างโฟลเดอร์:  mkdir -p .github/workflows 
2. เขียนไฟล์  .yml  วางลงไป
3. Commit & Push ขึ้น repo
4. ไปที่แท็บ Actions ดูผลการทำงาน ✅
 
ต้องการเขียน workflow สำหรับอะไรเป็นพิเศษไหมครับ? เช่น ปรับใช้ขึ้น Vercel, ตรวจสอบความปลอดภัย, หรือสร้าง Release อัตโนมัติ 😊