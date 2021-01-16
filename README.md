# 12306 验证码识别服务

## 发布打包版本

费劲巴拉的删减到小于50M的压缩包，[码云发布地址](https://gitee.com/sobweb/py12306-ocr/releases/0.1)

### 分流Bypass
1. 修改本机hosts(路径: `C:\Windows\System32\drivers\etc\hosts`), 插入：`127.0.0.1 v2-no-secure-api.jsdama.com`
2. 打开Bypass，登录时的验证码手动操作
3. 如果系统有开代理，进入Bypass，`设置代理`-`禁用IE代理`
4. `config.toml`默认配置`port = 80`，启动`打码.bat`
5. `验证码设置`-`第三方厂商`，平台选`联众`，用户名/密码任意，`登录`，`测试打码`

### 订票助手
1. 将插件覆盖至订票助手目录
2. `设置`->`远程打码`->`远程打码引擎`--`本地打码`，用户名/密码任意，`登录`
3. 勾选登录远程打码(登录时自动打码)
4. 保存配置
5. 修改`config.toml`中`port = 8082`，启动`打码.bat`

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

监听config.toml文件配置的端口, 默认8082, 服务于py12306
```bash
python main.py 
```
模拟**若快**需要监听80端口, 按下面的方式直接运行, 或者修改config.toml中的端口后按上面的来:
```bash
python web.py
```
用于识别文字的模型文件较大，没有放在仓库中，第一次运行会自动进行联网下载，所以可能需要等待一会才能运行起来。

## 免费用ByPass第三方联众打码配置
需要手动更改本机hosts, 防小白给出目录: `C:\Windows\System32\drivers\etc`, 

任意文本编辑器打开 `hosts` 添加一行:

`127.0.0.1	v2-no-secure-api.jsdama.com`

ByPass第三方打码选"联众", 用户名密码任意, 登录, 测试...

需要吐槽一下ByPass, 为了推销自家的打码服务, 故意拖延第三方的打码响应时间(大约3~4s)

## 订票助手免费打码
采用若快的接口，`hosts`添加: `127.0.0.1   api.ruokuai.com`

远程打码配置选**若快答题**，用户名密码任意，登录，保存配置

## Thanks
所用的模型和算法均来自 [https://github.com/zhaipro/easy12306](https://github.com/zhaipro/easy12306) 十分感谢！

## License
[Apache License.](https://github.com/pjialin/12306-ocr/blob/master/LICENSE)

