# 华秋 PCB Active Manufacturing

### 在 KiCad 一键询价和下单

华秋 PCB Active Manufacturing 插件将帮助您：

- 从您的设计中提取关键制造参数
- 在 KiCad 内获取华秋的实时报价
- 生成 Gerber 文件并将其与您的个人电路板设置一起上传到华秋

上传完成后，您可以使用华秋 DFM 仔细检查您的制造文件，调整电路板参数，然后将其直接添加到您的华秋购物车。
![华秋插件](https://github.com/SYSUeric66/kicad-amf-plugin/blob/8318782634b7f8237bd4a650c37e4031e876e3a0/docs/amf.gif)

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

###一键 Gerber 生成并同步到订单页面

单击“下订单”按钮生成 Gerber 和 NC 钻孔文件，并将其与您的电路板参数一起直接上传到华秋的订单页面。

一切都是同步的，因此不需要额外的调整。当然，您可以随意更改网站上的设置，然后继续订购。

支持以下区域：

- 欧洲和美国：[NextPCB](https://www.nextpcb.com/pcb-quote)
- 中国大陆 [华秋 PCB](https://www.hqpcb.com/quote/)
- 日本：[JP.NextPCB](https://jp.nextpcb.com/pcb-quote#/pcb-quote/)

## 安装

从 **为包保留** 下载最新版本的 ZIP 文件，然后在 KiCad 中，从主窗口打开“插件和内容管理器”。最后，使用窗口底部的“从文件安装...”来安装 ZIP 文件。
![图片](https://github.com/HubertHQH/HQ-NextPCB/assets/125419974/97ef0ca3-380e-4f6f-a14b-6960271118fc)

### 关于华秋 PCB

华秋专注于可靠的多层 PCB 制造和组装，与 KiCad 一样，我们的目标是帮助工程师构建未来的电子产品。 华秋 PCB 正在与 KiCad 合作提供智能工具来简化从设计到物理产品的流程。华秋拥有 3 家主要从事原型设计、批量生产和 PCB 组装的工厂，并拥有超过 15 年的工程专业知识，相信我们的行业经验对于 KiCad 用户和 PCB 设计社区来说将是无价的。

我们是 [KiCad 白金赞助商](https://www.nextpcb.com/blog/kicad-nextpcb-platinum-sponsorship)。
