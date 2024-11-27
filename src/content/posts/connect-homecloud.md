---
title: 如何让你的服务器Always Online？
published: 2024-11-27
description: '让自己维护的服务器始终可以访问是一件比较难的事，如果遇到突发灾难：比如断网断电。但是除去这些我们可以使用多种技术手段来保障服务器的高可访问性'
image: 'assets/images/2024-11-27-23-55-13-image.png'
tags: [STUN, Zerotier, Cloudflared, FRP, IPv6]
category: '运维'
draft: false 
lang: ''
---

> 感谢Chat GPT支持本文

# 家庭服务器内网穿透的几种方法

为确保家庭服务器可以被公网访问，以下介绍几种主流内网穿透方法，并详细说明其适用场景、操作步骤和注意事项。

---

## 方法一：使用 STUN 实现内网穿透

### 原理简介

STUN（Session Traversal Utilities for NAT）是一种 NAT 穿越技术，利用 NAT 映射关系将内网服务暴露到公网。它适用于多级 NAT 环境，并支持 TCP 和 UDP 协议。

### 使用 Lucky 或 Natter 工具

无需搭建 STUN 服务器，推荐直接使用工具如 [Lucky](https://lucky666.cn/) 或 [Natter](https://github.com/MikeWang000000/Natter)。这些工具通过 STUN 协议与服务端通信，动态映射您的内网服务到公网 IP 和随机端口。

#### 优点

- **无需额外配置：** 即开即用，适合应急。
- **支持多协议：** 同时支持 TCP 和 UDP。

#### 局限性

- **端口和 IP 不可控：** 每次映射的公网 IP 和端口随机分配，不适合长期稳定使用。

#### 网络拓扑

互联网 -> 共享公网 IPv4（运营商 NAT）-> 工具分配的公网 IP 和端口 -> 内网设备

---

## 方法二：使用 IPv6 实现内网穿透

### 原理简介

IPv6 拥有足够多的地址空间，通常无需 NAT，直接分配公网 IPv6 地址给用户。通过直接连接 IPv6 网络，可实现内网穿透。

### 操作步骤

1. **确认 IPv6 地址类型：**
   
   - 公网 IPv6（如 `240c::` 为电信，`2409::` 为移动，`2408::` 为联通）可直接被访问。
   - 内网 IPv6 通常为 `fd00::` 或 `fe80::` 开头，无法被公网访问。
   
   在 **Linux** 下运行 `ip a` 查看 IPv6 地址；在 **Windows** 中运行 `ipconfig` 或直接在设置中查看。

2. **关闭防火墙：**
   
   - **路由器：** 禁用 IPv6 防火墙。
   - **服务器：** 关闭防火墙规则，确保端口可被访问。

3. **确保对端支持 IPv6：**  
   对端设备或网络需具备 IPv6 连接能力。

4. **动态域名解析：**  
   使用工具如 [DDNS-GO](https://github.com/jeessy2/ddns-go) 绑定动态域名，方便在公网环境中定位 IPv6 地址。

#### 网络拓扑

互联网（IPv6 网络）-> 公网 IPv6 地址 -> 内网设备

---

## 方法三：使用 Cloudflared 隧道

#### 原理简介

Cloudflared 隧道通过 Cloudflare 的全球网络将内网服务暴露在公网，并利用其 ZeroTrust 安全功能保护连接。相比命令行，使用 Cloudflare 网页控制台创建和管理隧道更加直观和便捷。

在此方法中，Cloudflared 隧道不仅支持 HTTP/HTTPS 协议的内网穿透，也能支持 TCP 协议的服务（如 SSH 和 RDP）。但是，TCP 协议的服务需要在客户端和服务器端安装 Cloudflared 客户端。

---

### 操作步骤

#### **1. 激活 ZeroTrust 功能**

- 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)。
- 确保您的账户已绑定 PayPal 并激活 ZeroTrust 功能。

#### **2. 创建隧道**

1. **进入 ZeroTrust 控制台：**
- 在 Cloudflare Dashboard 中，导航到 **ZeroTrust 页面**。

- 点击 **Network -> Tunnels**，然后点击 **Create a tunnel**。
2. **安装 Cloudflared 客户端：**
- 在隧道创建页面，选择您服务器的操作系统（如 Linux 或 Windows）。

- 按照页面提供的命令，下载并安装 `cloudflared`：
  
  - **Linux 示例**：
    
    ```bash
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
    ```
  
  - **Windows 示例：** 直接下载可执行文件并运行。
3. **通过令牌完成安装：**
- 在创建隧道页面复制令牌安装命令。示例：
  
  ```bash
  cloudflared service install --token <your-token>
  ```

- 运行命令后，隧道会自动连接到 Cloudflare 全球网络，并在控制台显示为已激活。

#### **3. 配置隧道服务（以RDP为例）**

1. **创建子域（Public Hostname）：**
- 在隧道详情页面，选择 **Public Hostname**。

- 点击 **Create a Hostname**，填写以下信息：
  
  - **子域名：** 如 `rdp.example.com`。
  - **服务类型：** 选择 **RDP**。
  - **目标地址：** 输入 `localhost:3389`。
2. **保存配置：**  
   点击 **Save**，完成子域的配置。

#### **4. 客户端连接 RDP**

1. 在客户端设备上安装 `cloudflared`：
- 下载并安装与操作系统匹配的版本。

- 确保安装完成后能通过命令行调用 `cloudflared`。
2. **启动本地隧道：**  
   在客户端运行以下命令将远程 RDP 服务映射到本地端口：

```bash
cloudflared access rdp --hostname rdp.example.com --url rdp://localhost:3380
```

3. **远程桌面连接（mstsc）：**
- 打开 Windows 的 **远程桌面连接**工具（mstsc）。
- 在地址栏输入 `localhost:3380`，即可连接到远程服务器。

---

#### **管理与监控**

- 所有隧道和子域名可以在 **ZeroTrust -> Tunnels** 页面统一管理。
- 您可以随时通过控制台修改子域、服务类型或目标地址。

---

### 网络拓扑

互联网 -> Cloudflare 全球网络 -> 隧道服务 -> 本地 RDP

---

### 需要注意的事项

- **HTTP/HTTPS 服务**：Cloudflared 隧道非常适合 HTTP 和 HTTPS 流量，您可以通过配置 Web 服务来实现内网穿透而不需要在客户端和服务器端安装额外软件。

- **TCP 协议（SSH/RDP）**：对于非 HTTP/HTTPS 的服务（如 SSH、RDP），需要在客户端和服务器端都安装 Cloudflared 客户端，并通过相应命令将这些 TCP 服务暴露到 Cloudflare 网络上。

---

#### **官方文档**

详细的 Cloudflare ZeroTrust 和 Cloudflared 隧道设置文档可以参考 Cloudflare 官方文档：[Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

---

## 方法四：使用 Zerotier 组建虚拟局域网

### 原理简介

Zerotier 是一种虚拟局域网工具，可将分布式设备连入同一个虚拟网络，无需额外的公网 IP 或复杂配置。

### 操作步骤

1. **注册并安装：**
   
   - 在 Zerotier 官网（[zerotier.com](https://www.zerotier.com/)）注册账号并创建虚拟网络。
   - 在服务器和客户端分别安装 Zerotier 并加入网络。

2. **配置网络环境：**
   
   - 确保服务器端启用了 **UPnP** 、 **DMZ**或者设置 **端口转发**，将所有端口或者你需要的端口映射到服务器。

3. **测试连通性：**
   
   - 确保虚拟网络中的设备能够互相 ping 通。

#### 网络拓扑

Zerotier 虚拟局域网 -> 内网设备

---

## 方法5：使用 FRP 进行内网穿透（使用商业服务或者自建 FRP 服务）

FRP（Fast Reverse Proxy）是一个高效的内网穿透工具，能够将内网服务映射到公网，方便用户从外部访问内网设备。FRP 支持多种配置，既可以使用现成的商业服务，也可以自建服务端。以下是两种方式的详细介绍：

#### **1. 使用商业服务：樱花 FRP 和 Chmlfrp**

一些商业 FRP 服务提供商（如樱花 FRP 和 Chmlfrp）为用户提供稳定的内网穿透服务。这些服务允许用户快速连接到公网，但通常需要支付一定的费用，并且可能面临一定的安全风险，因为这些服务一般不使用高级安全防护措施。

- **优点**：随时可用，易于设置。
- **缺点**：需要支付费用，且可能容易遭受攻击。

#### **2. 自建 FRP 服务端**

如果您希望完全掌控内网穿透的过程，可以购买一个具有公网 IP 的服务器来自建 FRP 服务端。自建 FRP 服务端不仅可以完全控制数据流，还能根据自己的需求灵活配置。

**步骤：**

1. **购买服务器并安装 FRP**

首先，您需要购买一台具有公网 IP 的服务器（如 AWS、阿里云、腾讯云等），并确保有权限配置该服务器的防火墙和端口。然后，下载并安装 `frps`（FRP 服务端）。

2. **配置 FRP 服务端**

在服务端上配置 `frps.ini`，示例如下：

```ini
[common]
bind_port = 7000
vhost_http_port = 80
vhost_https_port = 443
```

3. **配置 FRP 客户端**

在内网设备上配置 `frpc.ini`，将内网服务映射到外网：

```ini
[common]
server_addr = 公网IP地址（frps服务器IP地址）
server_port = 7000

[rdp]
type = tcp
local_ip = 127.0.0.1
local_port = 3389
remote_port = 6000
```

4. **启动服务**

在服务端启动 `frps`：

```bash
./frps -c ./frps.ini
```

在客户端启动 `frpc`：

```bash
./frpc -c ./frpc.ini
```

#### **3. 启用身份验证**

为了确保安全，强烈建议启用身份验证，以防止未经授权的访问。FRP 提供了简单的 **Token 身份认证**，只需在 `frps.ini` 和 `frpc.ini` 中配置相同的 **token** 即可。[FRP 身份认证](https://gofrp.org/zh-cn/docs/features/common/authentication/)

**配置示例：**

- **frps.ini（服务端配置）**

```ini
[common]
bind_port = 7000
auth.token = "abc"  # 设置强令牌
```

- **frpc.ini（客户端配置）**

```ini
[common]
server_addr = 公网IP地址
server_port = 7000
auth.token = "abc"  # 使用与服务端相同的令牌
```

通过这种方式，您可以确保只有配置了正确令牌的客户端才能连接到 FRP 服务端，增加系统的安全性。

#### **4. 强化服务器安全性**

由于服务端暴露在公网，必须做好以下安全措施：

- **禁用弱密码和空密码**：确保所有账户使用强密码，避免使用空密码或弱密码。
- **启用防火墙**：确保只允许必要的端口（如 7000）和 IP 进行连接，其他端口和 IP 应被阻止。
- **定期更新软件**：保持 FRP 和服务器操作系统的更新，修补可能的安全漏洞。
- **使用 SSH 密钥登录**：如果通过 SSH 登录服务器，禁用密码登录并启用 SSH 密钥认证。
- **IP 白名单**：如果条件允许，设置 FRP 仅接受特定 IP 或 IP 范围的连接。

### **总结**

通过使用商业服务或自建 FRP 服务端，您可以实现强大的内网穿透功能。无论是使用简单的 Token 身份认证，还是加强安全防护，确保只有授权的用户才能访问内网服务，都是提高系统安全性的关键。自建服务端虽然需要额外配置和维护，但能够提供更高的自由度和安全性。如果您选择自建，务必注重安全措施，确保服务器不会受到外部攻击。

---

# 最终总结

最推荐使用 **Zerotier**，它提供了虚拟局域网功能，具备最高的安全性，并且在大多数环境下支持P2P连接，通常也是最快的连接方式。

为了确保服务器的高可访问性，我们建议采用多种故障修复方法。如果某些服务出现离线或故障，您可以通过 **Cloudflare Tunnel** 面板进行确认。通常来说，**cloudflared** 服务比较稳定，不容易掉线或崩溃。如果面板显示服务状态为 **HEALTHY**，那么您可以尝试通过 **RDP 隧道** 或 **SSH 隧道** 进行远程维护。如果显示为 **DOWN**，您应该首先进行物理接触服务器并排查错误。

总的来说，使用多种服务确保服务器的高可访问性非常重要。只要有一个服务仍然保持在线，其他服务就能够恢复和继续运行，从而保证系统的稳定性和可靠性。
