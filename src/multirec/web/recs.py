import streamlit as st

from multirec.web.exceptions import TooMuchResults
from multirec.web.utils import get_item_content, get_recs


def main_page():
    input_csv = "notebooks/Anime/data/extended_anime.csv"
    col = "Tags"

    df_with_recs = get_recs(input_csv, col)

    st.title('Аниме')
    
    form = st.form(key='search_from')
    title = form.text_input(label='Введите название...')
    submit_button = form.form_submit_button(label='Поиск')

    if submit_button:
        try:
            item = get_item_content(
                title,
                "Name",
                "recommendations",
                df_with_recs
            )
        except TooMuchResults as e:
            st.text(str(e))
            return

        st.markdown("# {}".format(item['title']))
        st.markdown('')
        st.markdown(item['desc'], unsafe_allow_html=True)
        st.markdown('')
        st.markdown('# Рекомендации')
        st.markdown("<br>".join(item['recs']), unsafe_allow_html=True)
