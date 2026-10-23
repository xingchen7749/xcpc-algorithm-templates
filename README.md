# XCPC 算法模板

## 📖 [点击阅读《算法模板手册》](ICPC_CCPC算法模板/算法模板手册.md)

完整算法讲解、模板代码、使用条件与易错点，按章节和算法目录快速跳转。

📄 [查看或下载 A4 打印版 PDF](output/pdf/算法模板手册_打印版.pdf)

---

面向 GNU C++17 的算法模板、中文手册与验证程序，涵盖基础技巧、数据结构、图论与树、字符串、数学、动态规划及计算几何。

- [使用说明](ICPC_CCPC算法模板/README.md)
- [算法模板要求](算法模板要求.md)：本项目对话、算法代码和手册维护的统一规范。
- [分章节阅读](ICPC_CCPC算法模板/章节/)
- [算法源码](ICPC_CCPC算法模板/代码/)
- [测试程序](ICPC_CCPC算法模板/测试/)
- [验证报告](ICPC_CCPC算法模板/验证报告.md)

## 维护与验证

`tools/` 集中保存生成源、附录和维护脚本；`ICPC_CCPC算法模板/` 保存手册、独立代码和测试；`output/pdf/` 保存打印版产物。

`tools/handbook_data.py` 保存条目内容，`tools/appendix.md` 保存附录。在项目根目录运行以下命令重新生成手册和算法文件：

```sh
python tools/build_handbook.py
```

项目同时提供打印版 PDF。更新手册后，在项目根目录运行以下命令生成打印版（首次使用需安装依赖）：

```sh
python -m pip install typst markdown-it-py
python tools/build_print_pdf.py
```

打印脚本读取 `ICPC_CCPC算法模板/算法模板手册.md`，将 PDF 和生成的 Typst 排版文件写入 `output/pdf/`。长期内容修改应维护生成源，再依次生成手册和打印版。

安装 Python 和 GNU C++17 编译器后，可验证独立程序：

```sh
python tools/verify_headers.py
```

详细用法、下标约定及测试命令见上述使用说明。

当前按“同一问题同一节、不同方法分小标题和独立文件”组织，共 85 份完整程序（含起手式）。运行 `python tools/verify_handbook.py` 可检查目录、代码链接、文件清单和重复生成一致性。
