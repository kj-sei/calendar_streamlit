import streamlit as st
import pandas as pd
import datetime
import streamlit_calendar as st_calendar
import json

# ページタイトル
st.title("予定表アプリ")

# JSONファイルからイベントを読み込む
with open('data.json') as file:
    events = json.load(file)
    
colors = ['blue','red','yellow','green','orange','purple','brown','gray','black']

# 予定の追加フォーム
with st.sidebar.form("予定追加フォーム"):
    start = st.date_input("開始日", datetime.date.today())
    end = st.date_input("終了日", datetime.date.today())
    color = st.selectbox("色を選択してください", colors)
    title = st.text_input("予定内容")
    
    submitted = st.form_submit_button("追加")

    if submitted and title:
        st.success("予定が追加されました")
        
        # 新しいイベントIDを計算
        id_num = events[-1]['id'] if events else 0
        data = {
            'id': id_num + 1,
            'editable': True,
            'start': start.isoformat(), 
            'end': end.isoformat(), 
            'title': title,
            'color': color
        }
        events.append(data)
        
        # JSONファイルにイベントを保存
        with open('data.json', 'w') as f:
            json.dump(events, f)

if events:
    # イベントリストからタイトルを抽出する
    event_titles = [event['title'] for event in events]

    with st.sidebar.form("削除フォーム"):
        delete_event = st.selectbox("削除する予定を選択してください", event_titles)
        submitted_delete = st.form_submit_button("削除")

        if submitted_delete:
            # 選択されたイベントを削除
            events = [event for event in events if event['title'] != delete_event]
            st.success("予定が削除されました")
            
            # JSONファイルにイベントを保存
            with open('data.json', 'w') as f:
                json.dump(events, f)




# カレンダーの表示
cal = st_calendar.calendar(events=events)
st.write(cal)
