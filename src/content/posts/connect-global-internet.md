---
title: 自建正向代理服务器
published: 2024-11-22
description: '不要再买机场了！自建它不香吗？!'
image: 'assets/images/2024-11-21-08-24-54-image.png'
tags: []
category: '教程'
draft: false 
lang: ''
---

# 将Cloudflare作为代理使用（Vless - EdgeTunnel）

下面内容参考自：[CF VLESS 从入门到精通 cmliu/edgetunnel 必看内容 免费节点 优选订阅 Workers & Pages CM喂饭干货满满24 | CMLiussss Blog](https://vercel.blog.cmliussss.com/p/CM24/) 请支持原创作者！

1. 进入 https://github.com/cmliu/edgetunnel/archive/refs/heads/main.zip 将它上传到你的Cloudflare Pages项目
2. 进入 https://it-tools.tech/uuid-generator 随机获取一个uuid
3. 添加一个名称为`UUID`的变量绑定，值为第二步随机获取的（请不要泄露给他人！）
4. 重新上传第一步的`main.zip`。让Cloudflare重新部署page以适配新变量
5. 绑定自定义域名。通过 https://你的自定义域名/uuid 查看仪表盘
6. 如图复制链接，打开V2Ray，导入。V2Ray客户端下载地址在文章最后
7. 懒人订阅器：`?sub=VLESS.fxxk.dedyn.io`。更多订阅器可以前往CM的Tg群获取，在顶上的CM博客中有
8. ![](assets/images/2024-11-24-00-17-22-image.png)
9. 500Mbps的移动宽带，通过edgetunnel测速速度如下
10. ![](assets/images/2024-11-22-09-08-38-image.png)
11. 如果你就是想要最低延迟，可以去用cfnat，这里放一个Windows的链接： https://www.youtube.com/watch?v=N2Y9TsiBgls 其他平台可以自行前往CM的YouTube查找
12. **注意！edgetunnel近期在Cloudflare新号上可能会报错1101，这可能并不是你的配置问题，而是被cf风控了。解决方案是删除原项目重新部署一遍，不要用一样的项目名！你也可以多弄几个其他的正常pages或workers项目做伪装**

# 将你自己的国外VPS作为代理使用

## 新协议：Hysteria2

可以前往这两个仓库进行一键安装~

::github{repo="0x0129/hysteria2"}

::github{repo="seagullz4/hysteria2"}

大致安装过程：自签名，不使用acme，不使用端口跳跃

客户端（Hiddify）：

::github{repo="hiddify/hiddify-app"}

其他客户端在第二个Github Repo获取

## 旧协议：V2Ray

::github{repo="233boy/v2ray"}

VPS安装脚本：`bash <(curl -s -L https://git.io/v2ray.sh)`

详细安装：脚本执行完毕后输入`v2ray`更改配置为Shadowsocks

Windows客户端： [Releases · 2dust/v2rayN · GitHub](https://github.com/2dust/v2rayN/releases)

Android客户端： [Releases · 2dust/v2rayNG · GitHub](https://github.com/2dust/v2rayNG/releases)
