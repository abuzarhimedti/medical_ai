import streamlit_authenticator as stauth
import streamlit as st
import ai_engine
import json
import os
from datetime import datetime


st.set_page_config(page_title="نظام sudan 249  الطبي الذكي", page_icon="🏥", layout="wide")

# ── Themes ───────────────────────────────────────────
THEMES = {
    "light": {
        "bg": "#F8FFF9", "surface": "#FFFFFF", "surface2": "#F0F7F4",
        "text": "#1A3A2A", "muted": "#5A7A6A", "border": "#C6E6D0",
        "primary": "#2E9E5B", "primary_dark": "#1B6B3A",
        "header_grad": "linear-gradient(135deg, #1B6B3A, #2E9E5B)",
        "card_bg": "#FFFFFF", "input_bg": "#FFFFFF",
        "sidebar_bg": "#F0F7F4", "shadow": "rgba(27,107,58,0.12)",
    },
    "dark": {
        "bg": "#0D1117", "surface": "#161B22", "surface2": "#21262D",
        "text": "#E6EDF3", "muted": "#7D8590", "border": "#30363D",
        "primary": "#00B4BD", "primary_dark": "#007B7F",
        "header_grad": "linear-gradient(135deg, #0D2B45, #007B7F)",
        "card_bg": "#161B22", "input_bg": "#21262D",
        "sidebar_bg": "#161B22", "shadow": "rgba(0,0,0,0.3)",
    },
    "green": {
        "bg": "#0A1F0F", "surface": "#112218", "surface2": "#193D24",
        "text": "#D4EDDA", "muted": "#7AAF85", "border": "#2E6B3E",
        "primary": "#4CAF50", "primary_dark": "#2E7D32",
        "header_grad": "linear-gradient(135deg, #1B5E20, #4CAF50)",
        "card_bg": "#112218", "input_bg": "#193D24",
        "sidebar_bg": "#0D1A11", "shadow": "rgba(76,175,80,0.15)",
    },
}

# ── Session State ────────────────────────────────────
defaults = {
    "theme": "light", "page": "🏠 الرئيسية",
    "stage": 1, "stage1_result": None,
    "symptoms": None, "patient": None,
    "labs_results": {}, "final_result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

T = THEMES[st.session_state.theme]

# ── CSS ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
* {{ font-family: 'Cairo', sans-serif !important; }}
.stApp {{ direction: rtl; background: {T['bg']}; color: {T['text']}; }}
section[data-testid="stSidebar"] {{ background: {T['sidebar_bg']} !important; border-left: 2px solid {T['border']}; }}
.main-header {{
    background: {T['header_grad']};
    padding: 2rem; border-radius: 16px; text-align: center;
    margin-bottom: 1.5rem; box-shadow: 0 8px 32px {T['shadow']};
}}
.card {{
    background: {T['card_bg']}; border-radius: 12px;
    padding: 1.2rem 1.4rem; margin: 0.6rem 0;
    border-right: 5px solid {T['primary']};
    box-shadow: 0 2px 12px {T['shadow']};
    color: {T['text']};
}}
.card-danger  {{ border-right-color: #E53E3E !important; }}
.card-success {{ border-right-color: {T['primary']} !important; }}
.card-warn    {{ border-right-color: #D69E2E !important; }}
.stButton > button {{
    background: {T['header_grad']} !important;
    color: white !important; border-radius: 10px !important;
    border: none !important; font-weight: 700 !important;
    box-shadow: 0 4px 15px {T['shadow']} !important;
}}
.stTextInput input, .stTextArea textarea {{
    background: {T['input_bg']} !important;
    color: {T['text']} !important;
    border: 2px solid {T['border']} !important;
    border-radius: 10px !important; direction: rtl !important;
}}
.nav-btn {{
    display: block; width: 100%; text-align: right;
    padding: 12px 18px; margin: 4px 0;
    border-radius: 10px; cursor: pointer;
    border: none; font-size: 15px; font-weight: 600;
    font-family: 'Cairo', sans-serif;
    transition: all 0.2s;
}}
.nav-btn-active {{
    background: {T['primary']}; color: white;
}}
.nav-btn-inactive {{
    background: transparent; color: {T['muted']};
}}
.nav-btn-inactive:hover {{ background: {T['surface2']}; color: {T['text']}; }}
.stat-card {{
    background: {T['card_bg']}; border-radius: 14px;
    padding: 1.4rem; text-align: center;
    box-shadow: 0 2px 12px {T['shadow']};
    border-top: 4px solid {T['primary']};
}}
div[data-testid="stMarkdownContainer"] {{ direction: rtl; text-align: right; }}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 8px">
        <div style="font-size:42px">🏥</div>
        <div style="font-size:15px;font-weight:900;color:{T['primary']}">نظام التشخيص الذكي</div>
        <div style="font-size:11px;color:{T['muted']};margin-top:2px">AI Medical Diagnosis</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Navigation
    st.markdown(f"<div style='font-size:12px;color:{T['muted']};font-weight:700;letter-spacing:1px;padding:4px 0'>القائمة الرئيسية</div>", unsafe_allow_html=True)

    pages = ["🏠 الرئيسية", "📋 سجل المرضى", "📊 الإحصائيات", "⚙️ الإعدادات", "ℹ️ عن النظام"]
    for pg in pages:
        is_active = st.session_state.page == pg
        style = "nav-btn-active" if is_active else "nav-btn-inactive"
        if st.button(pg, key=f"nav_{pg}", use_container_width=True):
            st.session_state.page = pg
            st.rerun()

    st.divider()

    # Theme switcher
    st.markdown(f"<div style='font-size:12px;color:{T['muted']};font-weight:700;letter-spacing:1px;padding:4px 0'>🎨 المظهر</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☀️ فاتح", use_container_width=True):
            st.session_state.theme = "light"; st.rerun()
    with col2:
        if st.button("🌙 داكن", use_container_width=True):
            st.session_state.theme = "dark"; st.rerun()
    with col3:
        if st.button("🌿 أخضر", use_container_width=True):
            st.session_state.theme = "green"; st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:11px;color:{T['muted']};text-align:center'>أبو ذر محمد المرضي<br>طالب هندسة طبية · 2025</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# PAGE: الرئيسية
# ════════════════════════════════════════════════════
if st.session_state.page == "🏠 الرئيسية":
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color:white;font-size:2rem;margin:0">🏥 نظام التشخيص الطبي الذكي</h1>
        <p style="color:rgba(255,255,255,0.8);margin:0.5rem 0 0">من الأعراض إلى التشخيص — بذكاء، دقة، وسرعة</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress steps
    stage = st.session_state.stage
    steps = [("🩺","الأعراض"), ("🔬","الفحوصات"), ("🧬","نتائج المختبر"), ("📊","التشخيص")]
    cols = st.columns(4)
    for i, (col, (icon, label)) in enumerate(zip(cols, steps)):
        with col:
            if i+1 < stage:
                st.success(f"✅ {icon} {label}")
            elif i+1 == stage:
                st.info(f"🔵 {icon} {label}")
            else:
                st.markdown(f"<div style='color:{T['muted']};padding:8px;text-align:center'>⚪ {icon} {label}</div>", unsafe_allow_html=True)
    st.divider()

    # ── Stage 1 ──
    if st.session_state.stage == 1:
        st.markdown("### 🩺 بيانات المريض والأعراض")
        patient_name = st.text_input("👤 اسم المريض", placeholder="اختياري")
        c1, c2 = st.columns(2)
        with c1:
            age     = st.text_input("🎂 العمر", placeholder="مثال: 28")
            chronic = st.text_input("💊 أمراض مزمنة", placeholder="اتركه فارغاً إن لم يوجد")
        with c2:
            gender   = st.selectbox("⚧ الجنس", ["ذكر", "أنثى"])
            duration = st.text_input("⏱️ مدة الأعراض", placeholder="مثال: يومان")
        symptoms = st.text_area("📝 صف الأعراض بالتفصيل", height=120,
            placeholder="مثال: صداع شديد، حمى 39 درجة، ألم في الحلق...")
        st.markdown('<div class="card card-warn">⚕️ للمساعدة الأولية فقط — لا يُغني عن الطبيب</div>', unsafe_allow_html=True)

        if st.button("🤖 تحليل بالذكاء الاصطناعي", use_container_width=True):
            if not symptoms.strip():
                st.error("يرجى إدخال الأعراض")
            else:
                with st.spinner("⏳ جاري التحليل..."):
                    patient = {"name": patient_name, "age": age, "gender": gender, "chronic": chronic, "duration": duration}
                    result  = ai_engine.analyze_symptoms(symptoms, patient)
                    if result:
                        st.session_state.stage=2; st.session_state.stage1_result=result
                        st.session_state.symptoms=symptoms; st.session_state.patient=patient
                        st.rerun()
                    else:
                        st.error("حدث خطأ في الاتصال ... راجع باقة الإنترنت ")

    # ── Stage 2 ──
    elif st.session_state.stage == 2:
        res = st.session_state.stage1_result
        if not res:
            st.session_state.stage=1; st.rerun()

        sev = res.get("خطورة","عادي")
        sev_cls = "card-danger" if sev=="طوارئ" else "card-warn" if sev=="عاجل" else "card-success"
        sev_icon = "🚨" if sev=="طوارئ" else "⚠️" if sev=="عاجل" else "✅"

        st.markdown(f'<div class="card {sev_cls}">{sev_icon} <strong>مستوى الخطورة: {sev}</strong></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card">📋 <strong>التحليل:</strong> {res.get("تحليل","")}</div>', unsafe_allow_html=True)

        for d in res.get("تشخيصات_مبدئية",[]):
            p = d.get("احتمالية",""); c = "#E53E3E" if p=="عالية" else "#D69E2E" if p=="متوسطة" else T['primary']
            st.markdown(f'<div class="card"><span style="color:{c}">●</span> <strong>{d.get("اسم","")}</strong> — {p}</div>', unsafe_allow_html=True)

        st.markdown("### 🧪 الفحوصات المطلوبة")
        for lab in res.get("فحوصات",[]):
            s = "⭐" if lab.get("أهمية")=="أساسي" else "🔹"
            st.markdown(f'<div class="card">{s} <strong>{lab.get("اسم","")} [{lab.get("رمز","")}]</strong><br><small>{lab.get("سبب","")} | طبيعي: {lab.get("طبيعي","")}</small></div>', unsafe_allow_html=True)

        if st.button("📋 إدخال نتائج الفحوصات ←", use_container_width=True):
            st.session_state.stage=3; st.rerun()

        st.divider()
        st.markdown("### 🔍 فحوصات إضافية")
        extra = st.text_area("أضف معلومات إضافية", placeholder="مثال: تعرضت لحقنة، مخالط لمريض...", key="extra")
        if st.button("🔬 طلب فحوصات إضافية", use_container_width=True):
            if extra.strip():
                with st.spinner("⏳ جاري التحليل..."):
                    r2 = ai_engine.analyze_symptoms(st.session_state.symptoms + " | " + extra, st.session_state.patient)
                    if r2:
                        orig = st.session_state.stage1_result.get("فحوصات",[])
                        exist = [l.get("اسم") for l in orig]
                        added = [l for l in r2.get("فحوصات",[]) if l.get("اسم") not in exist]
                        orig.extend(added)
                        st.session_state.stage1_result["فحوصات"] = orig
                        st.success(f"✅ تم إضافة {len(added)} فحص جديد!" if added else "الفحوصات الحالية كافية")
                        if added: st.rerun()

    # ── Stage 3 ──
    elif st.session_state.stage == 3:
        res  = st.session_state.stage1_result or {}
        labs = res.get("فحوصات",[])
        st.markdown("### 🧬 أدخل نتائج الفحوصات")
        lab_results = {}
        for lab in labs:
            name=lab.get("اسم",""); normal=lab.get("طبيعي","")
            s = "⭐" if lab.get("أهمية")=="أساسي" else "🔹"
            val = st.text_input(f"{s} {name} (طبيعي: {normal})", placeholder="اكتب النتيجة", key=f"lab_{name}")
            if val.strip(): lab_results[name]={"رمز":lab.get("رمز"),"قيمة":val,"طبيعي":normal}

        if st.button("✅ الحصول على التشخيص النهائي", use_container_width=True):
            if not lab_results:
                st.warning("أدخل نتيجة فحص واحدة على الأقل")
            else:
                with st.spinner("⏳ جاري التشخيص..."):
                    final = ai_engine.final_diagnosis(st.session_state.symptoms, st.session_state.patient, st.session_state.stage1_result, lab_results)
                    if final:
                        st.session_state.final_result=final; st.session_state.labs_results=lab_results
                        st.session_state.stage=4; st.rerun()
                    else: st.error("حدث خطأ")

    # ── Stage 4 ──
    elif st.session_state.stage == 4:
        final = st.session_state.final_result
        if not final: st.session_state.stage=1; st.rerun()

        st.markdown('<div class="card card-success">✅ <strong>اكتمل التحليل</strong></div>', unsafe_allow_html=True)
        diag = final.get("تشخيص_نهائي",{})
        if diag:
            st.markdown(f"""<div class="card card-success">
                <h3 style="color:{T['primary']}">✅ {diag.get('اسم','')}</h3>
                <p>الدرجة: <strong>{diag.get('درجة','')}</strong> | الثقة: <strong>{diag.get('ثقة','')}</strong></p>
                <p style="margin-top:6px">{diag.get('سبب','')}</p>
            </div>""", unsafe_allow_html=True)

        for item in final.get("تفسير_نتائج",[]):
            s=item.get("حالة",""); icon="✅" if s=="طبيعي" else "🔺" if s=="مرتفع" else "🔻"
            st.markdown(f'<div class="card">{icon} <strong>{item.get("فحص","")}:</strong> {item.get("قيمة","")} — {item.get("دلالة","")}</div>', unsafe_allow_html=True)

        plan = final.get("علاج",{})
        if plan:
            st.markdown("### 💊 خطة العلاج")
            c1,c2 = st.columns(2)
            with c1:
                st.markdown("**الأدوية:**")
                for m in plan.get("أدوية",[]): st.markdown(f"- 💊 {m}")
            with c2:
                st.markdown("**التوصيات:**")
                for r in plan.get("توصيات",[]): st.markdown(f"- ✅ {r}")
            if plan.get("متابعة"): st.success(f"📅 {plan['متابعة']}")
            if plan.get("تخصص"):   st.success(f"👨‍⚕️ {plan['تخصص']}")

        st.markdown('<div class="card card-warn">⚕️ هذا التشخيص أولي ولا يُغني عن الطبيب المختص</div>', unsafe_allow_html=True)

        # Save record
        hf = "patients_history.json"
        hist = json.load(open(hf,"r",encoding="utf-8")) if os.path.exists(hf) else []
        rec = {"اسم": st.session_state.patient.get("name","مجهول") if st.session_state.patient else "مجهول",
               "تاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
               "أعراض": st.session_state.symptoms or "",
               "تشخيص": diag.get("اسم","") if diag else "", "خطة_علاج": plan}
        if not any(r.get("تاريخ")==rec["تاريخ"] for r in hist):
            hist.append(rec)
            json.dump(hist, open(hf,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

        if st.button("🔄 فحص حالة جديدة", use_container_width=True):
            for k in ["stage","stage1_result","symptoms","patient","labs_results","final_result"]:
                st.session_state[k] = defaults[k]
            st.rerun()

# ════════════════════════════════════════════════════
# PAGE: سجل المرضى
# ════════════════════════════════════════════════════
elif st.session_state.page == "📋 سجل المرضى":
    st.markdown(f'<div class="main-header"><h2 style="color:white;margin:0">📋 سجل المرضى</h2></div>', unsafe_allow_html=True)

    hf = "patients_history.json"
    if os.path.exists(hf):
        hist = json.load(open(hf,"r",encoding="utf-8"))
        if hist:
            st.markdown(f"**إجمالي الحالات:** {len(hist)}")
            st.divider()
            for i, rec in enumerate(reversed(hist)):
                with st.expander(f"👤 {rec.get('اسم','مجهول')}  —  {rec.get('تاريخ','')}  |  🔬 {rec.get('تشخيص','')}"):
                    st.write(f"**الأعراض:** {rec.get('أعراض','')}")
                    st.write(f"**التشخيص:** {rec.get('تشخيص','')}")
                    plan = rec.get("خطة_علاج",{})
                    if plan.get("أدوية"):
                        st.write("**الأدوية:**")
                        for m in plan["أدوية"]: st.write(f"  - {m}")
            if st.button("🗑️ مسح كل السجلات"):
                os.remove(hf); st.success("تم مسح السجلات"); st.rerun()
        else:
            st.info("لا يوجد سجلات بعد")
    else:
        st.info("لا يوجد سجلات بعد — ابدأ بفحص حالة جديدة")

# ════════════════════════════════════════════════════
# PAGE: الإحصائيات
# ════════════════════════════════════════════════════
elif st.session_state.page == "📊 الإحصائيات":
    st.markdown(f'<div class="main-header"><h2 style="color:white;margin:0">📊 الإحصائيات</h2></div>', unsafe_allow_html=True)

    hf = "patients_history.json"
    if os.path.exists(hf):
        hist = json.load(open(hf,"r",encoding="utf-8"))
        if hist:
            total = len(hist)
            diagnoses = [r.get("تشخيص","غير محدد") for r in hist]
            from collections import Counter
            counts = Counter(diagnoses).most_common(5)

            c1,c2,c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="stat-card"><div style="font-size:36px;font-weight:900;color:{T["primary"]}">{total}</div><div style="color:{T["muted"]}">إجمالي الحالات</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="stat-card"><div style="font-size:36px;font-weight:900;color:{T["primary"]}">{len(set(diagnoses))}</div><div style="color:{T["muted"]}">أنواع التشخيصات</div></div>', unsafe_allow_html=True)
            with c3:
                today = datetime.now().strftime("%Y-%m-%d")
                today_count = sum(1 for r in hist if r.get("تاريخ","").startswith(today))
                st.markdown(f'<div class="stat-card"><div style="font-size:36px;font-weight:900;color:{T["primary"]}">{today_count}</div><div style="color:{T["muted"]}">حالات اليوم</div></div>', unsafe_allow_html=True)

            st.markdown("### 🔝 أكثر التشخيصات شيوعاً")
            for diag, count in counts:
                pct = int(count/total*100)
                st.markdown(f"""
                <div class="card" style="margin:6px 0">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span style="color:{T['primary']};font-weight:700">{count} حالة ({pct}٪)</span>
                        <span style="font-weight:600">{diag}</span>
                    </div>
                    <div style="background:{T['border']};border-radius:4px;height:6px;margin-top:8px">
                        <div style="background:{T['primary']};width:{pct}%;height:6px;border-radius:4px"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات كافية للإحصائيات")
    else:
        st.info("لا توجد بيانات — ابدأ بفحص حالات أولاً")

# ════════════════════════════════════════════════════
# PAGE: الإعدادات
# ════════════════════════════════════════════════════
elif st.session_state.page == "⚙️ الإعدادات":
    st.markdown(f'<div class="main-header"><h2 style="color:white;margin:0">⚙️ الإعدادات</h2></div>', unsafe_allow_html=True)

    st.markdown("### 🎨 المظهر")
    theme_names = {"light": "☀️ فاتح", "dark": "🌙 داكن", "green": "🌿 أخضر داكن"}
    selected = st.radio("اختر المظهر", list(theme_names.values()),
        index=list(theme_names.keys()).index(st.session_state.theme))
    for k,v in theme_names.items():
        if v == selected and k != st.session_state.theme:
            st.session_state.theme = k; st.rerun()

    st.divider()
    st.markdown("### 🗄️ البيانات")
    hf = "patients_history.json"
    if os.path.exists(hf):
        hist = json.load(open(hf,"r",encoding="utf-8"))
        st.info(f"يوجد {len(hist)} حالة محفوظة")
        if st.button("🗑️ مسح جميع السجلات", type="primary"):
            os.remove(hf); st.success("تم مسح السجلات بنجاح"); st.rerun()
        col1, col2 = st.columns(2)
        with col1:
            data = json.dumps(hist, ensure_ascii=False, indent=2)
            st.download_button("📥 تحميل السجلات JSON", data, "patients_history.json", "application/json")
    else:
        st.info("لا توجد سجلات محفوظة")

# ════════════════════════════════════════════════════
# PAGE: عن النظام
# ════════════════════════════════════════════════════
elif st.session_state.page == "ℹ️ عن النظام":
    st.markdown(f'<div class="main-header"><h2 style="color:white;margin:0">ℹ️ عن النظام</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card card-success">
        <h3 style="color:{T['primary']}">🏥 نظام الطبي الذكي</h3>
        <p>نظام ذكي يجمع بين الأعراض والنتائج المخبرية لتقديم تشخيص طبي أولي دقيق.</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚙️ التقنيات المستخدمة")
        techs = [("🐍","Python 3.12"), ("🖥️","Streamlit"), ("🤖","LLaMA 3.3 70B"), ("⚡","Groq API")]
        for icon, tech in techs:
            st.markdown(f'<div class="card" style="padding:10px 14px">{icon} {tech}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📋 مراحل العمل")
        stages = [("1️⃣","إدخال الأعراض"), ("2️⃣","تحليل AI واقتراح فحوصات"), ("3️⃣","إدخال نتائج المختبر"), ("4️⃣","التشخيص النهائي")]
        for num, stage in stages:
            st.markdown(f'<div class="card" style="padding:10px 14px">{num} {stage}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:1.5rem">
        <div style="font-size:18px;font-weight:900;color:{T['primary']}">أبو ذر محمد المرضي</div>
        <div style="color:{T['muted']};margin-top:4px">طالب هندسة طبية · 2025</div>
        <div style="margin-top:8px;font-size:13px;color:{T['muted']}">⚕️ للمساعدة الأولية فقط — لا يُغني عن الطبيب المختص</div>
    </div>""", unsafe_allow_html=True)