# 春联快闪生成器 🧧

AI驱动的春节春联创作工具，输入3个关键词，生成专属春联，分享领红包！

## 🌟 功能特性

- ✨ **AI智能创作**：基于GPT的春联生成
- 🎨 **精美UI**：春节红金配色，传统与现代结合
- 🧧 **红包活动**：分享春联领现金红包
- 📱 **一键分享**：生成精美分享文案
- ⏰ **春节倒计时**：实时显示距离春节还有多久

## 🚀 在线体验

**Streamlit Cloud部署地址**：
```
https://springcouplet-flash.streamlit.app
```

## 📦 本地安装

### 环境要求
- Python 3.8+
- OpenAI API Key

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/linqunhao/springcouplet-flash.git
cd springcouplet-flash

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app_v2.py
```

## 🎯 使用方法

1. **输入OpenAI API Key**（在侧边栏设置）
2. **填写3个关键词**（如：升职、买房、健康）
3. **点击"生成我的专属春联"**
4. **截图分享到朋友圈/小红书**
5. **添加微信领红包！**

## 🧧 红包活动

- **活动资金**：¥200
- **红包数量**：20个
- **每人金额**：¥10
- **参与方式**：
  1. 生成春联
  2. 截图分享到社交平台
  3. 添加微信：`CloverAI_2026`
  4. 发送截图领取红包

## 🛠️ 技术栈

- **前端**：Streamlit
- **AI引擎**：OpenAI GPT-3.5/GPT-4
- **部署**：Streamlit Cloud / Cloudflare Tunnel

## 📄 文件结构

```
springcouplet-flash/
├── app.py              # 基础版本
├── app_v2.py           # 完整版本（推荐）
├── requirements.txt    # 依赖列表
├── deploy_public.py    # 公网部署脚本
├── start_tunnel.sh     # Cloudflare隧道启动脚本
└── README.md           # 本文件
```

## 🎨 界面预览

![春联生成器界面](screenshot.png)

## 📝 更新日志

### v2.0 (2026-02-13)
- ✨ 新增春节豪华UI
- 🧧 新增红包活动功能
- 🎊 新增飘雪动画效果
- ⏰ 新增春节倒计时
- 📱 优化分享功能

### v1.0 (2026-02-13)
- 🎉 首个版本发布
- ✨ AI春联生成功能
- 💾 基础分享功能

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系我们

- **微信**：CloverAI_2026
- **邮箱**：linqunhao@gmail.com

## 📜 许可证

MIT License

---

🎊 **祝大家新春快乐，万事如意！** 🎊
