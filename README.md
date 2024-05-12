# DDL Report

生成 postgresql ddl 报告

## 安装

```bash
pip install -e .
```

## 测试

```bash
python -m unittest
```

## 生成exe

```bash
# 需要提前安装好 pyinstaller
pyinstaller -F .\ddl_report.py
```

## 使用

```bash
./ddl_report.exe './db'
```

# 获取帮助

```bash
./ddl_report.exe -h
```
