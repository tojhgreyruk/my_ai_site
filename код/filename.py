import streamlit as st
from fpdf import FPDF

# Заголовок
st.set_page_config(page_title="Клієнтоорієнтований аналіз", layout="centered")
st.title("🔍 Аналіз TikTok профілю")

# Ввод посилання
tiktok_url = st.text_input("Встав посилання на TikTok профіль:")

# Фейкові дані (щоб працювало на Streamlit Cloud)
fake_user_data = {
    "Ім'я": "Аня",
    "Любить": "солодощі, подорожі, квіти",
    "Місця, куди хоче поїхати": "Париж, Балі",
    "Ідеї для подарунків": "книга, сертифікат в SPA, квитки на концерт",
    "Статус": "Можливо у відносинах"
}

def generate_report(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Аналіз TikTok профілю", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.multi_cell(0, 10, f"{key}: {value}")

    return pdf

# Кнопка аналізу
if st.button("🔎 Проаналізувати"):
    if not tiktok_url:
        st.warning("Будь ласка, встав посилання на профіль TikTok.")
    else:
        st.success("✅ Дані отримано (тестові). Ось що ми дізнались:")
        for key, value in fake_user_data.items():
            st.write(f"**{key}**: {value}")

        # Завантаження PDF
        pdf = generate_report(fake_user_data)
        pdf.output("tiktok_report.pdf")
        with open("tiktok_report.pdf", "rb") as f:
            st.download_button("📄 Завантажити PDF звіт", f, file_name="звіт.pdf")
