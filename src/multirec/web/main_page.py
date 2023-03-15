import os

import streamlit as st

from multirec.web.utils import search_title, get_recs, get_item_by_id
from multirec.web.utils import parse_line_dict


def main_page(input_csv):
    mappings = os.environ.get('MAPPINGS', None)
    if mappings:
        mappings = parse_line_dict(mappings)
    index = os.environ.get('INDEX', None)

    df_with_recs = get_recs(input_csv, mappings=mappings, index=index)

    st.markdown(
        "<h1 style='text-align: center;'>{}</h1>".format('Multirec is all you need'),
        unsafe_allow_html=True
    )
    
    form = st.form(key='search_from')
    title = form.text_input(label='Введите название...')
    submit_button = form.form_submit_button(
        label='Поиск')
        
    query_params = st.experimental_get_query_params()
    if submit_button:
        st.experimental_set_query_params(
            item_title=title
        )
        st.experimental_rerun()
    elif 'item_title' in query_params:
        search(query_params['item_title'][0], df_with_recs)
    elif 'item_id' in query_params:
        item_id = int(query_params['item_id'][0])
        show_item(item_id, df_with_recs)
        

def search(title, df_with_recs):
    items = search_title(
        title,
        df_with_recs
    )
    items = list(map(
        lambda x: '<a href="/?item_id={}">{}</a>'.format(x[0], x[1]), 
        items)
    )
    st.markdown("<br>".join(items), unsafe_allow_html=True)


def show_item(item_id, df_with_recs):
    item = get_item_by_id(item_id, df_with_recs)

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
        lambda x: '<a href="/?item_id={}">{}</a>'.format(x[0], x[1]), 
        item['recs'])
    )
    st.markdown("<br>".join(item['recs']), unsafe_allow_html=True)
