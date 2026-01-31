import streamlit as st
from zhipuai import ZhipuAI
import time

# ================= 配置区域 =================
# ⚠️ 填入你的 Key
API_KEY = "c2cd9f6ca9394c5c9284d5d547cb5cc4.yJxCm9sJ8tR11N3H"
# ===========================================

# 初始化客户端
try:
    client = ZhipuAI(api_key=API_KEY)
except:
    pass


def generate_ecom_prompt(user_input):
    """
    电商实景摄影导演 v9.0 (纯实景/不分段/精细构图)
    """

    # 错误拦截
    if not API_KEY or "请在这里" in API_KEY:
        return "❌ 错误：请在代码中填入正确的 API Key"

    # 1. 扩容后的角度库
    angle_list = """
    [ 正面 (Front view), 侧面 (Side profile), 四分之三侧面 (3/4 Side view), 四分之一侧面 (1/4 Side view),
    背面 (Back view), 回头/回眸 (Looking back), 
    小角度俯视 (Slight high angle), 小角度仰视 (Slight low angle), 平视 (Eye level) ]
    """

    # 2. 核心 System Prompt
    system_instruction = f"""
    你是一位对光影和构图有极致追求的电商摄影导演。
    用户输入服装产品，请**自主设计**一套完整的电商实景拍摄指令。

    **输入产品**：{user_input}
    **核心风格**：电商实景大片，光线充足，模特皮肤白皙哑光，少高光。

    请严格执行以下决策逻辑，并最终**整合成一段话输出**：

    1. **背景策略 (智能实景)**：
       - 根据服装风格自主匹配场景（如：CBD街头/美术馆/极简咖啡店/公园）。
       - **虚化控制**：采用 **f/4.0 或 f/5.6 光圈**。背景轻度虚化以突出模特，但**背景轮廓和纹理必须依然清晰**，严禁过度虚化。
       - **避坑**：画面中**严禁**出现柔光箱、三脚架、反光板等摄影设备。

    2. **形象与肤质**：
       - 自动识别性别：柔美/裙装 -> **中国女模**；中性/工装 -> **中国男模**。
       - **肤质铁律**：皮肤**白皙透亮**，妆容为**高级哑光雾面**，**少高光**，零油光。男模**绝对无胡须**。

    3. **穿搭与鞋履 (完整性)**：
       - **强制补全**：卖上衣必须自主搭配下装；卖下装必须自主搭配上衣。
       - **鞋子**：凡是全身或下半身构图，**必须穿鞋**。根据风格自主匹配（运动/休闲/潮牌/流行）。

    4. **机位与构图 (关键)**：
       - **上衣** -> **膝盖以上 (Knee-up)**。
       - **裤子/裙子** -> 根据展示效果自主选择 **全身照 (Full body)** 或 **下半身特写 (Lower body shot)**（重点展示裤型和鞋子）。
       - **角度调度**：从以下角度库中自主选择一个最生动的：{angle_list}。动作要自然松弛，不死板。

    **输出格式要求**：
    **请直接输出一段连贯的中文描述，不要分段，不要加标题，不要有换行。** 
    (例如：一张高级感的电商街拍，模特为中国女模...身穿...搭配...背景为...采用f/5.6光圈...)
    """

    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"请为【{user_input}】生成一段连贯的拍摄指令"}
            ],
            temperature=0.8,
            top_p=0.85
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API 调用出错: {e}"


# ================= 🎨 UI 界面 (极简版) =================

st.set_page_config(
    page_title="电商实景摄影导演",
    page_icon="🎬",
    layout="wide"
)

# 隐藏默认元素
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTextArea textarea {font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

# 历史记录
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- 侧边栏 ---
with st.sidebar:
    st.title("🎬 实景导演")
    st.caption("E-commerce Scene Director v9.0")
    st.markdown("---")
    st.info("💡 当前模式：**全自动智能实景**")

    st.markdown("---")
    st.subheader("📜 最近记录")
    if st.session_state['history']:
        for item in reversed(st.session_state['history'][-5:]):
            st.text_area(f"🕒 {item['time']} - {item['input']}", value=item['result'], height=150)

# --- 主界面 ---
st.title("电商实景模特图生成器")
st.markdown("#### 🤖 Auto-Director for Chinese E-commerce Scene")
st.success("✅ 已启用：下装补全 | 智能轻度虚化 | 下半身特写逻辑 | 连贯段落输出")

# 输入区
col_input, col_tips = st.columns([3, 1])

with col_input:
    user_input = st.text_input("👗 请输入服装名称", placeholder="例如：浅蓝色垂感阔腿裤 / 美式复古棒球服")

    if st.button("🚀 生成实景拍摄指令", type="primary", use_container_width=True):
        if not user_input:
            st.toast("⚠️ 请输入内容！")
        else:
            with st.spinner("🧠 导演正在构思场景与穿搭..."):
                start_time = time.time()
                result = generate_ecom_prompt(user_input)

                # 存历史
                st.session_state['history'].append({
                    "time": time.strftime("%H:%M"),
                    "input": user_input,
                    "result": result
                })

                st.toast(f"✅ 生成成功！", icon="🎉")

                # 结果展示
                st.markdown("### 📸 拍摄指令")
                st.info("👇 直接复制整段话即可：")
                st.container(border=True).code(result, language="text")

with col_tips:
    with st.container(border=True):
        st.markdown("##### 📌 核心策略")
        st.markdown("""
        - **构图**：
          裤子可拍全身或下半身特写。
        - **角度**：
          新增背面、1/4侧面、小仰视等。
        - **输出**：
          一段话，无分段。
        """)