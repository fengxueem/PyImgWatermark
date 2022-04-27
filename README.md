# PyImgWatermark

这是一个脚本的简单项目，实现多线程给大批量 JPG 图像打上统一文字水印。水印文字保持不变，但水印个数、颜色、位置、文字角度为随机生成。
## 目录

- [背景](#背景)
- [依赖](#编译)
- [用法](#用法)
- [主要项目负责人](#主要项目负责人)
- [参与贡献方式](#参与贡献方式)
    - [贡献人员](#贡献人员)
- [开源协议](#开源协议)

## 依赖

请在 python3 环境中安装以下依赖。
```shell
argparse
OpenCV
tqdm
numpy
```

## 用法

脚本接受 3 个参数，示例用法和参数说明如下。

```shell
python addwatermarks.py --in-img-dir /home/gohgih/in_data/ --out-img-dir /home/gohgih/data/ --watermark-txt @foo.bar
```

|参数名称|类型|方向|说明|
|--|--|--|--|
|in-img-dir|合法路径|输入|输入图片路径，脚本会深度遍历路径下所有 jpg 图片|
|out-img-dir|合法路径|输入|输出图片路径，该路径下会完整保存输入图片路径中的目录结构|
|watermark-txt|字符串|输入|水印文字|

## 主要项目负责人

[@fengxueem](https://github.com/fengxueem)

## 参与贡献方式

欢迎 PR。

### 贡献人员

感谢所有作出贡献的开发人员。

[@fengxueem](https://github.com/fengxueem)

## 开源协议

暂未确定开源协议。

