import google.generativeai as genai
import os
from dotenv import load_dotenv

# تأكد من أن ملف .env موجود ويحتوي على GOOGLE_API_KEY صحيح
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("خطأ: مفتاح API غير موجود في ملف .env")
else:
    try:
        genai.configure(api_key=api_key)
        print("جاري الاتصال بسيرفرات جوجل...")

        # طباعة الموديلات المتاحة فقط
        models = [m.name for m in genai.list_models()]
        print("الموديلات المتاحة في حسابك هي:")
        for m in models:
            print(f"- {m}")

    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")