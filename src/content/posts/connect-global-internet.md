---
title: 自建正向代理服务器
published: 2024-11-21
description: '不要再买机场了！自建它不香吗？!'
image: 'assets/images/2024-11-21-08-24-54-image.png'
tags: []
category: '教程'
draft: false 
lang: ''
---

# 将Cloudflare作为代理使用（Vless）

1. 进入 https://github.com/yonggekkk/Cloudflare_vless_trojan/blob/main/Vless_workers_pages/_worker.js 这是Workers代码
2. 进入 https://it-tools.tech/uuid-generator 随机获取一个uuid
3. 在代码第七行写入你的uuid
4. 绑定自定义域名。通过https://你的自定义域名/uuid查看仪表盘

# 将你自己的国外VPS作为代理使用

## 新协议：Hysteria2

::github{repo="seagullz4/hysteria2"}

VPS安装脚本：`curl -sSL https://github.com/seagullz4/hysteria2/raw/main/install.sh -o install.sh && chmod +x install.sh && bash install.sh`

详细安装：自签名，不使用acme，不使用端口跳跃

客户端（Hiddify）：

::github{repo="hiddify/hiddify-app"}

其他客户端在第一个Github Repo获取

## 旧协议：V2Ray

::github{repo="233boy/v2ray"}

VPS安装脚本：`bash <(curl -s -L https://git.io/v2ray.sh)`

详细安装：脚本执行完毕后输入`v2ray`更改配置为Shadowsocks

Windows客户端： [Releases · 2dust/v2rayN · GitHub](https://github.com/2dust/v2rayN/releases)

Android客户端： [Releases · 2dust/v2rayNG · GitHub](https://github.com/2dust/v2rayNG/releases)
