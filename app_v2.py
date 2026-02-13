# SpringCouplet Flash - 春联快闪生成器 v2.0
# 美化版 + 红包功能

import streamlit as st
from groq import Groq
import random
import json
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="春联快闪生成器 - 春节红包版",
    page_icon="🧧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 初始化session state
if 'couplet_generated' not in st.session_state:
    st.session_state.couplet_generated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = random.randint(100000, 999999)
if 'hongbao_claimed' not in st.session_state:
    st.session_state.hongbao_claimed = False

# 自定义CSS - 春节豪华版
st.markdown("""
<style>
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #1a0000 0%, #4a0000 50%, #8B0000 100%);
        background-attachment: fixed;
    }
    
    /* 主标题 */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 0 0 20px rgba(255,215,0,0.5);
        margin-bottom: 10px;
        font-family: 'STKaiti', 'KaiTi', 'Microsoft YaHei', serif;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 0 0 20px rgba(255,215,0,0.5); }
        to { text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 0 0 30px rgba(255,215,0,0.8), 0 0 40px rgba(255,215,0,0.6); }
    }
    
    /* 副标题 */
    .subtitle {
        text-align: center;
        color: #FFA500;
        font-size: 18px;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* 红包区域 */
    .hongbao-section {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(255,215,0,0.3);
        border: 3px solid #8B0000;
        text-align: center;
    }
    
    .hongbao-title {
        font-size: 24px;
        color: #8B0000;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .hongbao-amount {
        font-size: 36px;
        color: #DC143C;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(255,215,0,0.5);
    }
    
    /* 输入框样式 */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.1);
        border: 2px solid #FFD700;
        border-radius: 10px;
        color: #FFD700;
        font-size: 16px;
        padding: 10px;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255,215,0,0.6);
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% 200%;
        color: #8B0000;
        border: none;
        border-radius: 30px;
        padding: 18px 40px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(255,215,0,0.4);
        transition: all 0.3s;
        animation: shine 3s ease-in-out infinite;
    }
    
    @keyframes shine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(255,215,0,0.6);
    }
    
    /* 对联展示框 */
    .couplet-display {
        background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 0 60px rgba(255,215,0,0.1);
        border: 4px solid #FFD700;
        position: relative;
        overflow: hidden;
    }
    
    .couplet-display::before {
        content: "🧧";
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 30px;
        opacity: 0.3;
    }
    
    .couplet-display::after {
        content: "🧧";
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 30px;
        opacity: 0.3;
    }
    
    /* 横批 */
    .horizontal-scroll {
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        color: #8B0000;
        font-size: 32px;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-family: 'STKaiti', 'KaiTi', serif;
        letter-spacing: 8px;
    }
    
    /* 上下联 */
    .vertical-text {
        writing-mode: vertical-rl;
        text-orientation: upright;
        font-size: 36px;
        color: #FFD700;
        font-weight: bold;
        letter-spacing: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        font-family: 'STKaiti', 'KaiTi', serif;
        line-height: 1.8;
        padding: 20px;
    }
    
    /* 倒计时 */
    .countdown-box {
        background: rgba(255,215,0,0.1);
        border: 2px dashed #FFD700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .countdown-number {
        font-size: 48px;
        color: #FFD700;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* 装饰元素 */
    .decoration {
        text-align: center;
        font-size: 40px;
        margin: 10px 0;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* 分享区域 */
    .share-section {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    
    /* 底部 */
    .footer {
        text-align: center;
        color: rgba(255,215,0,0.7);
        font-size: 14px;
        margin-top: 40px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 装饰元素
def add_decorations():
    st.markdown("<div class='decoration'>🎊 🏮 🎊</div>", unsafe_allow_html=True)

# 标题
add_decorations()
st.markdown("<h1 class='main-title'>🧧 春联快闪生成器 🧧</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI为你写春联 · 分享领红包</p>", unsafe_allow_html=True)
add_decorations()

# 春节倒计时
spring_festival = datetime(2026, 2, 16)
days_left = (spring_festival - datetime.now()).days
hours_left = int((spring_festival - datetime.now()).seconds / 3600)

st.markdown(f"""
<div class='countdown-box'>
    <p style='color: #FFA500; margin: 0;'>🎉 距离春节还有</p>
    <div class='countdown-number'>{days_left}天 {hours_left}小时</div>
    <p style='color: #FFD700; margin: 0;'>快来生成你的专属春联，分享领红包！</p>
</div>
""", unsafe_allow_html=True)

# 红包活动区域
st.markdown("---")
st.markdown("""
<div class='hongbao-section'>
    <div class='hongbao-title'>🧧 春节红包活动 🧧</div>
    <p style='color: #4a0000; font-size: 16px; margin: 10px 0;'>
        分享你的春联到朋友圈/小红书<br>
        截图发给客服，即可领取红包！
    </p>
    <div class='hongbao-amount'>¥200</div>
    <p style='color: #8B0000; font-size: 14px;'>剩余红包：<strong>20</strong> 个 | 每人 <strong>¥10</strong></p>
    <p style='color: #666; font-size: 12px; margin-top: 10px;'>
        活动规则：生成春联 → 截图分享 → 添加微信领取
    </p>
</div>
""", unsafe_allow_html=True)

# 侧边栏 - API设置
with st.sidebar:
    st.markdown("### ⚙️ 设置")
    api_key = st.text_input("Groq API Key", type="password", 
                           value=os.getenv("OPENAI_API_KEY", ""))
    
    st.markdown("---")
    st.markdown("### 📖 使用步骤")
    steps = [
        "1️⃣ 输入3个关键词（如：升职、买房、健康）",
        "2️⃣ 点击生成春联",
        "3️⃣ 截图保存或复制文案",
        "4️⃣ 分享到朋友圈/小红书",
        "5️⃣ 添加微信领红包！"
    ]
    for step in steps:
        st.markdown(f"<p style='color: #FFD700; font-size: 13px; margin: 8px 0;'>{step}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📞 联系客服")
    st.markdown("<p style='color: #FFD700; text-align: center;'>微信：CloverAI_2026</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFA500; font-size: 12px; text-align: center;'>分享后截图发给客服领红包</p>", unsafe_allow_html=True)

# 主界面 - 输入区域
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #FFD700; margin-bottom: 20px;'>✨ 输入你的2025关键词</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    keyword1 = st.text_input("", placeholder="如：升职 💼", key="k1", label_visibility="collapsed")
with col2:
    keyword2 = st.text_input("", placeholder="如：买房 🏠", key="k2", label_visibility="collapsed")
with col3:
    keyword3 = st.text_input("", placeholder="如：健康 💪", key="k3", label_visibility="collapsed")

# 生成按钮
if st.button("🎯 生成我的专属春联", use_container_width=True):
    if not api_key:
        st.error("⚠️ 请先输入Groq API Key（在左侧设置中）")
    elif not all([keyword1, keyword2, keyword3]):
        st.warning("⚠️ 请填写3个关键词")
    else:
        with st.spinner("🎨 AI正在挥毫泼墨..."):
            try:
                # 使用Groq API
                client = Groq(api_key=api_key)
                
                # 生成对联
                prompt = f"""你是一位精通中华传统文化的对联大师。请根据以下3个关键词，创作一副优美、吉祥、有文化底蕴的春联：

关键词：{keyword1}、{keyword2}、{keyword3}

要求：
1. 上联7个字，下联7个字，横批4个字
2. 必须巧妙融入关键词的含义
3. 平仄相对，对仗工整
4. 寓意吉祥，适合春节氛围
5. 语言优美，有文学性
6. 横批要画龙点睛

请按以下格式输出：
上联：[7个字]
下联：[7个字]
横批：[4个字]
解读：[简要说明对联的寓意和巧妙之处]"""
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=300
                )
                
                result = response.choices[0].message.content
                
                # 解析结果
                lines = result.strip().split('\n')
                upper = ""
                lower = ""
                horizontal = ""
                explanation = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("上联：") or line.startswith("上联:"):
                        upper = line.replace("上联：", "").replace("上联:", "").strip()
                    elif line.startswith("下联：") or line.startswith("下联:"):
                        lower = line.replace("下联：", "").replace("下联:", "").strip()
                    elif line.startswith("横批：") or line.startswith("横批:"):
                        horizontal = line.replace("横批：", "").replace("横批:", "").strip()
                    elif line.startswith("解读：") or line.startswith("解读:") or line.startswith("解释：") or line.startswith("解释:"):
                        explanation = line.replace("解读：", "").replace("解读:", "").replace("解释：", "").replace("解释:", "").strip()
                
                # 保存到session
                st.session_state.couplet_data = {
                    'upper': upper,
                    'lower': lower,
                    'horizontal': horizontal,
                    'explanation': explanation,
                    'keywords': [keyword1, keyword2, keyword3]
                }
                st.session_state.couplet_generated = True
                
            except Exception as e:
                st.error(f"❌ 生成失败：{e}")

# 展示对联
if st.session_state.couplet_generated and 'couplet_data' in st.session_state:
    data = st.session_state.couplet_data
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #FFD700; margin-bottom: 20px;'>🎉 你的专属春联</h3>", unsafe_allow_html=True)
    
    # 对联展示框
    st.markdown("<div class='couplet-display'>", unsafe_allow_html=True)
    
    # 横批
    st.markdown(f"<div class='horizontal-scroll'>{data['horizontal']}</div>", unsafe_allow_html=True)
    
    # 上下联
    col_left, col_spacer, col_right = st.columns([2, 1, 2])
    with col_left:
        st.markdown(f"<p class='vertical-text' style='text-align: center; margin-left: 40%;'>{data['upper']}</p>", unsafe_allow_html=True)
    with col_right:
        st.markdown(f"<p class='vertical-text' style='text-align: center; margin-right: 40%;'>{data['lower']}</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 解读
    if data['explanation']:
        st.markdown(f"""
        <div style='background: rgba(255,215,0,0.1); border-left: 4px solid #FFD700; padding: 15px; border-radius: 10px; margin: 20px 0;'>
            <p style='color: #FFA500; margin: 0; font-weight: bold;'>💡 对联寓意</p>
            <p style='color: #FFD700; margin: 10px 0 0 0;'>{data['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 分享区域
    st.markdown("<div class='share-section'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #FFD700; text-align: center;'>📱 分享领红包</h4>", unsafe_allow_html=True)
    
    # 分享文案
    share_text = f"""🧧 我的AI专属春联 🧧

上联：{data['upper']}
下联：{data['lower']}
横批：{data['horizontal']}

💭 关键词：{data['keywords'][0]}、{data['keywords'][1]}、{data['keywords'][2]}

由「春联快闪生成器」AI创作
扫码生成你的专属春联，还有红包领！

#春联快闪 #AI创作 #春节红包 #专属春联"""
    
    st.text_area("复制分享文案 👇", share_text, height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="💾 下载文案",
            data=share_text,
            file_name="我的春联.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("🎁 我要领红包", use_container_width=True):
            st.info("🧧 添加微信：CloverAI_2026\n发送截图即可领取红包！")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 温馨提示
    st.markdown("""
    <div style='background: linear-gradient(90deg, rgba(255,215,0,0.2), rgba(255,165,0,0.2)); border-radius: 10px; padding: 15px; margin-top: 20px; text-align: center;'>
        <p style='color: #FFD700; margin: 0; font-size: 16px;'>🎊 分享你的春联到朋友圈/小红书，截图发给客服领红包！</p>
        <p style='color: #FFA500; margin: 5px 0 0 0; font-size: 14px;'>剩余红包有限，先到先得！</p>
    </div>
    """, unsafe_allow_html=True)

# 底部
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p style='font-size: 20px; margin: 10px 0;'>🎊 🏮 🐍 🏮 🎊</p>
    <p>祝大家新春快乐，蛇年大吉！</p>
    <p style='font-size: 12px; margin-top: 20px;'>Powered by OpenAI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

# 飘雪效果（JavaScript）
st.markdown("""
<script>
// 简单的飘雪效果
const snowflakes = ['❄️', '🧧', '🏮', '✨'];
function createSnowflake() {
    const flake = document.createElement('div');
    flake.innerText = snowflakes[Math.floor(Math.random() * snowflakes.length)];
    flake.style.position = 'fixed';
    flake.style.left = Math.random() * 100 + 'vw';
    flake.style.top = '-50px';
    flake.style.fontSize = Math.random() * 20 + 15 + 'px';
    flake.style.opacity = Math.random() * 0.5 + 0.3;
    flake.style.pointerEvents = 'none';
    flake.style.zIndex = '9999';
    flake.style.animation = `fall ${Math.random() * 3 + 2}s linear`;
    document.body.appendChild(flake);
    
    setTimeout(() => {
        flake.remove();
    }, 5000);
}

setInterval(createSnowflake, 300);

// 添加CSS动画
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)
