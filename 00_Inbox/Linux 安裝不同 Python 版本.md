---
tags: ['Linux', 'Python', 'Installation']
---
## 安裝

當你完成 Ubuntu 環境時，他會內建 python，很多系統級別的程序
都會需要依靠內建的 python 所以再不改動的情況下又要下載特定版本需要一套複雜流程

- 步驟一：安裝建構工具
```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

- 安裝 Git
```bash
sudo apt install git -y
```

- 使用 `pyenv` 安裝 Python 版本
```bash
curl https://pyenv.run | bash
```

- 加入環境變數
```bash
cat >> ~/.bashrc <<'EOF'
# >>> pyenv init >>>
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
EOF
```

- 加入 bash 啟動檔
```bash
source ~/.bashrc
```

- 安裝 Python 3.12.9 並設為預設
```bash
pyenv install 3.12.9
pyenv global 3.12.9
```

- 查看系統所有環境
```
pyenv versions
```

- 刪除版本
```bash
pyenv uninstall 3.11.8
```

---
## 驗證

安裝完成後，打開 命令提示字元(CMD) 或 PowerShell，輸入：
```bash
python3 --version
pip --version
```

若能顯示 Python 與 pip 版本號，即代表安裝成功。 預期：
```bash
Python 3.x.x
pip 23.x.x
```