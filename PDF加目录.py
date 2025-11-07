from typing import Generator
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import IndirectObject
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AddCatalog:
    catalog_str: str  # 目录字符串, 用于提取目录信息
    pdf_path: Path  # PDF文件路径
    offset: int = 0  # 页码偏移量, 用于调整目录页码与实际页码的差异
    split_page: str = "P"  # 分割页面标识, 指定目录页中的页面分割字符
    split_grade: str = "."  # 页面级别标识, 用于指定目录中的页面级别分隔符
    out_path: Path | None = None  # 输出文件路径，未指定则默认为原文件路径加"(目录)"后缀

    def page_add_offset(self, catalog: str) -> tuple[str, int]:
        """
        此方法分解目录字符串为页面名称和页面编号, 并加上预设的偏移量.
        :param catalog: 原始目录字符串, 包含页码信息.
        """
        # 分解目录字符串为页面名称和页面编号
        page_name, page_num = catalog.split(self.split_page, 1)
        page_name = page_name.strip()
        # 将页面编号转换为索引并加上页码偏移量，从0开始计数
        page_num = int(page_num.strip()) + self.offset - 1
        return (page_name, page_num)

    def catalog_add_offset(self) -> Generator[tuple[str, int]]:
        """
        遍历目录字符串(catalog_str), 将其按行分割, 调用page_add_offset方法对行进行处理.
        """
        for catalog in self.catalog_str.split("\n"):
            catalog = catalog.strip()
            if not catalog:  # 跳过空行
                continue
            yield self.page_add_offset(catalog)

    def main(self) -> None:
        """
        给PDF添加目录功能.
        解析PDF中的页面, 为其添加对应的目录层级, 并在PDF文档中添加对应的目录结构.
        方法依赖于PdfReader和PdfWriter类来读取和写入PDF内容, 以及catalog_add_offset()方法来获取目录页面信息.
        """

        writer = PdfWriter()
        # 复制原PDF的所有页面到新PDF中
        for page in PdfReader(self.pdf_path).pages:
            writer.add_page(page)

        # 初始化目录级别列表，以存储每个级别的目录项引用
        grade_list: list[IndirectObject | None] = [None]
        for page_name, page_num in self.catalog_add_offset():
            # 计算页面所属的级别，基于特定字符(self.split_grade)在页面名称中的出现次数
            page_grade = page_name.count(self.split_grade) + 1
            # 如果当前级别超过已初始化的级别数量，则扩展级别列表
            if page_grade >= len(grade_list):
                grade_list.append(None)
            # 在writer对象中添加目录项，并通过引用维护每个级别的目录结构
            grade_list[page_grade] = writer.add_outline_item(
                title=page_name,
                page_number=page_num,
                parent=grade_list[page_grade - 1],
            )
        # 写入带有新目录结构的PDF文件
        out_path = self.out_path or Path(
            self.pdf_path.with_stem(f"{self.pdf_path.stem}(目录)")
        )
        with open(out_path, "wb") as fout:
            writer.write(fout)


if __name__ == "__main__":
    pdf = Path(r"D:\study\programming\sourse.pdf")
    '''
    目录格式如下
    catalog_str = """
    封面 P-7
    前言 P-4
    目录 P-2
    chapter 1 源石, 天灾, 矿石病 P1
        1.1源石 P2
        1.2源石技艺 P9
        1.3天灾 P15
            1.3.1天灾信使 P21
        1.4矿石病 P25
    chapter 2 泰拉科技 P33
        2.1 源石技术 P34
        2.2 工业科技：移动城市 P42
            2.2.1 第一座现代移动城市 P51
        2.3 武器与装备 P53
    """
    '''
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
