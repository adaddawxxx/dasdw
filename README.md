# Lenovo_auto_signin

联想商城每日自动签到获取延保

如何使用：

Fork本项目，Secrets添加环境变量`USERNAME`和`PASSWORD`

如需实现server酱推送，需要添加环境变量`PUSH_KEY`

在Actions中运行

不支持多用户，仅支持用户名+密码登录方式

博客图文教程：https://www.locjj.com/bug/12.html

2021.02.08更新：添加server酱推送微信消息，用于提示用户是否完成签到

2021.02.08更新：添加腾讯云云函数（SCF）支持，详细教程看上方图文教程
