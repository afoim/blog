---
title: 利用阿里云云函数 FC 搭建AList后端，每月仅需5毛！
published: 2024-11-02
description: '阿里云云函数 FC是一个弹性的计算平台，可托管多种服务。搭配AList的前后端分离部署，实现比VPS更低的价格，得到更好的体验'
image: 'assets/images/47518d4403328a0fcb716f0e06fc7f608e6c65b7.png'
tags: [阿里云云函数 FC]
category: '开发'
draft: false 
lang: ''
---



先下载AList最新版的Linux-amd64可执行文件，并将其放到一个空文件夹：[Release Latest · AlistGo/alist · GitHub](https://github.com/AlistGo/alist/releases/latest)![2024-11-02-02-44-06-image.png](assets/images/4cb7fda890a3c06a995bc109711ce2a52c57f3d7.png)

前往：[函数计算 FC](https://fcnext.console.aliyun.com/overview)

选择创建函数![2024-11-02-02-42-18-image.png](assets/images/47c33b21f3cfb9cf6f05c8f63bfb9c7d2e7ef3d7.png)

创建一个Web函数，如图填写信息。然后创建![2024-11-02-02-44-52-image.png](assets/images/f82baf09877ded25583bb46427e6664455d18f73.png)

进入已经创建完毕的函数控制面板![2024-11-02-02-45-23-image.png](assets/images/4a0be482e97f7761fc37c49c0d7b55e1b6ed5777.png)

依次进入 代码 -> Terminal -> New Terminal

![2024-11-02-02-47-41-image.png](assets/images/62195f4becb769407e608b330568172fc60a96d1.png)

输入`./alist server`并复制临时密码，随后我们点击黄色按钮部署代码![2024-11-02-02-48-24-image.png](assets/images/5891603b4a0db141410fb04932fbf167c9ec0c66.png)

来到 配置 -> 触发器 复制公网HTTPS地址。这就是你的AList后端地址，如果你有备案域名，可绑定自定义域名来实现访问。如果你没有，可以将其作为后端API使用，在Cloudflare Pages部署AList_Web项目即可，教程：[教你把AList的前端部署到CF Pages！让你的AList秒加载！](/posts/alist-web-for-cf-page/)
