# git set up
git config --global user.name "CharlesTin0122"
git config --global user.email tianchao0533@gmail.com

## git 支持代理，如果你自己有一些ss工具的话，可直接让git走代理。

git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890
注意：这是全局代理，且socks5的端口是1080，请注意自己的本地端口是否是1080。

## 检查配置是否生效：

git config --global --get http.proxy
git config --global --get https.proxy

## 如果想取消使用代理，可以输入以下命令：

git config --global --unset http.proxy
git config --global --unset https.proxy
重新clone一遍，速度会有极大提升。
