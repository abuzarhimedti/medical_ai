import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = res.choices[0].message.content.strip()
    if "```" in text :
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def analyze_symptoms(symptoms, patient):
    prompt = f"""أنت طبيب ذكي تعايين مرضى في السودان مع إنتشار أمراض كالملاريا و الضنكو التايفوييد و الإلتهابات المختلفة و غيرها من الأمراض. أجب فقط بـ JSON بدون أي نص إضافي:
{{"تحليل":"وصف الحالة","تشخيصات_مبدئية":[{{"اسم":"...","احتمالية":"عالية"}}],"خطورة":"عادي","فحوصات":[{{"اسم":"...","رمز":"CBC","سبب":"...","طبيعي":"...","أهمية":"أساسي"}}],"تعليمات":"..."}}

العمر: {patient.get('age')} | الجنس: {patient.get('gender')} | الأعراض: {symptoms}"""
    try:
        return ask_ai(prompt)
    except Exception as e:
        print(f"خطأ: {e}")
        return None

def final_diagnosis(symptoms, patient, stage1, labs):
    prompt = f"""أنت طبيب ذكي. أجب فقط بـ JSON بدون أي نص إضافي:
{{"تفسير_نتائج":[{{"فحص":"...","قيمة":"...","حالة":"طبيعي","دلالة":"..."}}],"تشخيص_نهائي":{{"اسم":"...","درجة":"خفيف","ثقة":"85%","سبب":"..."}},"علاج":{{"أدوية":["..."],"توصيات":["..."],"متابعة":"...","تخصص":"..."}},"تحذيرات":[]}}

الأعراض: {symptoms}
نتائج الفحوصات: {json.dumps(labs, ensure_ascii=False)}"""
    try:
        return ask_ai(prompt)
    except Exception as e:
        print(f"خطأ: {e}")
        return None