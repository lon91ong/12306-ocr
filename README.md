# 12306 验证码识别服务

## 使用
需要运行在 python 3.6 以上版本

**1. 安装依赖**
```bash
git clone https://github.com/pjialin/12306-ocr

pip install -r requirements.txt
```
**2. 配置程序**
```bash
cp config.toml.example config.toml
```
**3. 运行程序**
```bash
python main.py
```
用于识别文字的模型文件较大，没有放在仓库中，第一次运行会自动进行联网下载，所以可能需要等待一会才能运行起来。

## 免费用ByPass第三方联众打码配置
需要手动更改本机hosts, 防小白给出目录: `C:\Windows\System32\drivers\etc`, 

任意文本编辑器打开 `hosts` 添加一行:

`127.0.0.1	v2-no-secure-api.jsdama.com`

ByPass第三方打码选"联众", 用户名密码任意, 登录, 测试...

需要吐槽一下ByPass, 为了推销自家的打码服务, 故意拖延第三方的打码响应时间(大约3~4s)

## Thanks
所用的模型和算法均来自 [https://github.com/zhaipro/easy12306](https://github.com/zhaipro/easy12306) 十分感谢！

## License
[Apache License.](https://github.com/pjialin/12306-ocr/blob/master/LICENSE)

