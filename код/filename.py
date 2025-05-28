import streamlit as st
from TikTokApi import TikTokApi
from fpdf import FPDF

# Анализ текста — ищем ключевые слова
def analyze_text(text):
    keywords = {
        "подарок": ["подарок", "подарки", "хочу подарок", "подарить"],
        "путешествия": ["хочу поехать", "мечтаю", "отпуск", "путешествие", "поехать", "тур", "хочу в"],
        "отношения": ["люблю", "парень", "девушка", "отношения", "любовь", "встречаюсь"],
        "день рождения": ["день рождения", "праздник", "отметить", "др"],
    }
    found = {}
    text_lower = text.lower()
    for category, words in keywords.items():
        for w in words:
            if w in text_lower:
                found.setdefault(category, 0)
                found[category] += 1
    return found

# Создаём PDF отчёт в памяти
def create_pdf(report_dict, original_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Отчёт по TikTok профилю", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Исходный текст (описания видео):")
    pdf.set_font("Arial", style="I", size=11)
    pdf.multi_cell(0, 10, original_text)
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Выявленные интересы и желания:", ln=True)
    pdf.set_font("Arial", size=12)
    if report_dict:
        for k, v in report_dict.items():
            pdf.cell(0, 10, f"- {k.capitalize()}: найдено {v} упоминаний", ln=True)
    else:
        pdf.cell(0, 10, "Ничего не найдено.", ln=True)
    return pdf.output(dest='S').encode('latin1')

# Основной Streamlit интерфейс
st.title("Анализ TikTok профиля")

with st.form("tiktok_form"):
    username = st.text_input("Введите имя пользователя TikTok (без @)")
    submitted = st.form_submit_button("Собрать и проанализировать")

if submitted:
    if not username.strip():
        st.error("Пожалуйста, введите имя пользователя TikTok.")
    else:
        with st.spinner("Собираем данные с TikTok..."):
            try:
                api = TikTokApi()
                user_videos = api.user(username).videos(count=10)
                descriptions = []
                for video in user_videos:
                    desc = video.desc
                    if desc:
                        descriptions.append(desc)
                full_text = "\n".join(descriptions)

                if not full_text.strip():
                    st.warning("У этого пользователя нет описаний видео для анализа.")
                else:
                    st.subheader("Тексты из описаний видео:")
                    st.write(full_text)

                    # Анализ
                    result = analyze_text(full_text)
                    st.subheader("Результаты анализа:")
                    if result:
                        for cat, cnt in result.items():
                            st.write(f"- **{cat.capitalize()}**: {cnt} упоминаний")
                    else:
                        st.write("Ключевых интересов не обнаружено.")

                    # Создаём PDF и даём скачать
                    pdf_data = create_pdf(result, full_text)
                    st.download_button(
                        label="Скачать отчёт PDF",
                        data=pdf_data,
                        file_name=f"{username}_tiktok_report.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Ошибка при получении данных: {e}")
