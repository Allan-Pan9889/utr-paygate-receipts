本目录下的 DejaVuSans*.ttf 可由脚本拉取；因上游 DejaVu raw 链接不稳定，脚本会优先下载
Noto Sans（SIL OFL），仍保存为上述文件名供 ReportLab 注册为 PayGateSans*。

获取方式：
  python scripts/fetch_bundled_fonts.py

若未放置有效 ttf，将自动使用 PDF 内置 Helvetica，金额前缀显示为「Rs」。
