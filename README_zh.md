# HQ PCB

<p>
    中文 |<a href="README.md">English<a/>
</p>

### 在 KiCad 一键询价和下单

HQ PCB 插件将帮助您：

- 从您的设计中提取关键制造参数
- 在 KiCad 内获取华秋的实时报价
- 生成 Gerber 文件并将其与您的个人电路板设置一起上传到华秋

上传完成后，您可以使用华秋 DFM 仔细检查您的制造文件，调整电路板参数，然后将其直接添加到您的华秋购物车。
![HQ PCB插件](https://github.com/Huaqiu-Electronics/kicad-hqpcb-plugin/blob/main/docs/hqpcb-screen.gif)

## 特色

### 自动参数提取

启动插件时，将从您的 KiCad 设计中提取以下参数：

- 层数
- 电路板尺寸（x，y）
- 板厚
- 最小走线宽度/间距
- 最小钻孔尺寸

_注意：这些参数无法从插件中编辑，因为它们是直接从您的 KiCad 设计中提取的。_

### 直接在 KiCad 中获取实时报价

单击“更新价格”按钮，从华秋获取您的电路板的最新定价和交货时间。

您可以随时修改其他参数（例如阻焊层颜色、电路板数量等），然后单击按钮即可重新报价。所有选项均与[华秋 PCB](https://www.hqpcb.com/)同步。

_注意：某些组合受到限制（例如白色丝印不能与白色阻焊层一起选择）。_

### 一键 Gerber 生成并同步到订单页面

单击“下订单”按钮生成 Gerber 和 NC 钻孔文件，并将其与您的电路板参数一起直接上传到华秋的订单页面。

一切都是同步的，因此不需要额外的调整。当然，您可以随意更改网站上的设置，然后继续订购。

支持以下区域：
- 中国大陆 [华秋 PCB](https://www.hqpcb.com/quote/)

## 安装

从KiCad主窗口打开“扩展内容管理器”。然后，“KiCad official repository”中找到“HQ PCB”,进行安装安装。
![图片](https://github.com/Huaqiu-Electronics/kicad-hqpcb-plugin/blob/main/kicad_amf_plugin/icon/image.png)


## NextPCB

NextPCB为海外版本的HQ PCB ，支持日本、欧洲和美国下单。
- 欧洲和美国：[NextPCB](https://www.nextpcb.com/pcb-quote)
- 日本：[JP.NextPCB](https://jp.nextpcb.com/pcb-quote#/pcb-quote/)

## HQ DFM

HQ DFM 一键分析开短路、断头线、线距线宽等20余项设计风险问题。
[华秋DFM](https://dfm.hqpcb.com/)
您可以使用 HQ DFM 仔细检查您的制造文件，调整电路板参数。


### 关于华秋 PCB

华秋专注于可靠的多层 PCB 制造和组装，与 KiCad 一样，我们的目标是帮助工程师构建未来的电子产品。 华秋 PCB 正在与 KiCad 合作提供智能工具来简化从设计到物理产品的流程。华秋拥有 3 家主要从事原型设计、批量生产和 PCB 组装的工厂，并拥有超过 15 年的工程专业知识，相信我们的行业经验对于 KiCad 用户和 PCB 设计社区来说将是无价的。

我们是 [KiCad 白金赞助商](https://www.nextpcb.com/blog/kicad-nextpcb-platinum-sponsorship)。

## Credits

该项目包含副本或使用其他作品。这些作品及其各自的许可和条款是：
[kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools.git)  基于[MIT License](https://github.com/Bouni/kicad-jlcpcb-tools/blob/main/LICENSE)