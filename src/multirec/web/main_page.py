import streamlit as st

from multirec.web.exceptions import TooMuchResults, ItemNotFound
from multirec.web.utils import get_item_content, get_recs


def main_page(input_csv, mapping=None):
    df_with_recs = get_recs(input_csv, mapping=mapping)

    st.title('Аниме')
    
    form = st.form(key='search_from')
    title = form.text_input(label='Введите название...')
    submit_button = form.form_submit_button(label='Поиск')

    if submit_button:
        try:
            item = get_item_content(
                title,
                df_with_recs
            )
        except TooMuchResults as e:
            st.text(str(e))
            return
        except ItemNotFound as e:
            st.text(str(e))
            return
        

        st.markdown("# {}".format(item['title']))
        st.markdown('Тэги: {}'.format(item['tags']))
        st.markdown('')
        st.markdown('## Описание')
        st.markdown(item['desc'], unsafe_allow_html=True)
        st.markdown('')
        st.markdown('## Ссылки')
        st.markdown('[Источник]({})'.format(item['url']))
        st.markdown('')
        st.markdown('## Рекомендации')
        st.markdown("<br>".join(item['recs']), unsafe_allow_html=True)
