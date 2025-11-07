# PDF加目录工具

一个用于给PDF文件添加目录（书签）的Python工具。

## 功能介绍

该工具可以为没有目录的PDF文件添加可点击的目录结构（也称为书签），支持多级目录结构。通过指定目录文本和对应的页码，程序会自动在PDF文件中创建相应的书签结构。

## 使用方法

### 1. 安装依赖

```bash
pip install PyPDF2
```

### 2. 准备目录文本

目录文本需要按照特定格式编写：

```
封面 P1
版权页 P3
前言 P4
目录 P9
一 概率论的基本概念 P13
    1.1 随机试验 P13
    1.2 样本空间、随机事件 P14
    1.3 频率与概率 P17
    小结 P36
    习题 P37
二 随机变量及其分布 P42
    2.1 随机变量 P42
    2.2 离散型随机变量及其分布律 P44
```

其中：
- 每行表示一个目录项
- 层级关系基于特定字符(self.split_grade，默认为. )在页面名称中的出现次数。目录中不出现. 为一级标题，出现一个. 为二级标题
- 每行末尾使用 `P` + 页码 表示对应页码（可根据需要调整）
- 页码从1开始计算

### 3. 使用代码

```python
from pathlib import Path
from PDF加目录 import AddCatalog

# PDF文件路径
pdf_path = Path("your_file.pdf")

# 目录字符串
catalog_str = """
封面 P1
版权页 P3
前言 P4
"""

# 创建AddCatalog实例并执行
catalog = AddCatalog(
    catalog_str=catalog_str,
    pdf_path=pdf_path,
    offset=0  # 页码偏移量，根据实际情况调整
)
catalog.main()
```

### 参数说明

- `catalog_str`: 目录字符串，包含目录项和页码信息
- `pdf_path`: 原始PDF文件路径
- `offset`: 页码偏移量（可选，默认为0）
- `split_page`: 页码分隔符（可选，默认为"P"）
- `split_grade`: 层级分隔符（可选，默认为"."）
- `out_path`: 输出文件路径（可选，默认在原文件名后添加"(目录)"）

## 示例

```python
if __name__ == "__main__":
    pdf = Path(r"D:\study\programming\sourse.pdf")
    catalog_str = """
    封面 P1
    版权页 P3
    前言 P4
    目录 P9
    一 概率论的基本概念 P13
        1.1 随机试验 P13
        1.2 样本空间、随机事件 P14
        1.3 频率与概率 P17
        1.4 等可能模型（古典模型） P21
        1.5 条件概率 P27
        1.6 独立性 P33
        小结 P36
        习题 P37
    二 随机变量及其分布 P42
        2.1 随机变量 P42
        2.2 离散型随机变量及其分布律 P44
    """
    Catalog = AddCatalog(catalog_str=catalog_str, pdf_path=pdf, offset=0)
    Catalog.main()
```

## 注意事项

- 页码从1开始计数
- 层级关系基于特定字符(self.split_grade，默认为. )在页面名称中的出现次数
- 输出文件默认保存在原文件相同目录下，文件名后添加"(目录)"后缀
