name: Cmys_set

on:
  push:
    paths:
      - 'itv11.txt'   # 仅当该文件被修改时触发运行
    branches: [main]  # 限制只在主分支上触发运行
permissions:
  contents: write
  
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: pip install selenium requests futures eventlet

      - name: Run cctv
        run: python ${{ github.workspace }}/cctv.py

      - name: Run weishi
        run: python ${{ github.workspace }}/weishi.py

      - name: Run ktpd
        run: python ${{ github.workspace }}/ktpd.py
 
      - name: Run ysyl
        run: python ${{ github.workspace }}/ysyl.py

      - name: Run xiangang
        run: python ${{ github.workspace }}/xiangang.py

      - name: Run qita
        run: python ${{ github.workspace }}/qita.py

      - name: 提交总表更改
        run: |
          git config --local user.email "g832@x-zw.com"
          git config --local user.name "xzw832"
          git add .
          git commit cctv.txt -m "Add generated file"
          git commit weishi.txt -m "Add generated file"
          git commit ktpd.txt -m "Add generated file"
          git commit ysyl.txt -m "Add generated file"
          git commit qita.txt -m "Add generated file"
          git commit itvlist.txt -m "Add generated file"
          #git pull --rebase
          git push -f
