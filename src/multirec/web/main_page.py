import streamlit as st

from multirec.web.exceptions import TooMuchResults, ItemNotFound
from multirec.web.utils import get_item_content, get_recs


def main_page(input_csv, mapping=None):
    df_with_recs = get_recs(input_csv, mapping=mapping)

    st.title('Multirec')
    
    form = st.form(key='search_from')
    title = form.text_input(label='Введите название...')
    submit_button = form.form_submit_button(
        label='Поиск')
        
    query_params = st.experimental_get_query_params()
    if query_params:
        show_content(query_params['item_title'][0], df_with_recs)
    elif submit_button:
        st.experimental_set_query_params(
            item_title=title
        )
        st.experimental_rerun()
        

def show_content(title, df_with_recs):
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

    item['recs'] = list(map(
        lambda x: '<a href="/?item_title={}">{}</a>'.format(x, x), 
        item['recs'])
    )
    st.markdown("<br>".join(item['recs']), unsafe_allow_html=True)
