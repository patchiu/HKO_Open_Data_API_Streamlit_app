# Documents\Python\HKO_Open_Data_API_app
# streamlit run HKO_Open_Data_API_app.py

import streamlit as st
import requests
import pandas as pd
import datetime

st.set_page_config(layout="wide")
st.write("""
# HKO_Open_Data_API App
""")

st.write("""
Get the past data of 'Low Temperature', 'Average Temperature', 'Max Temperature' from HKO_Open_Data_API.
""")
st.write('-'*10)


location = st.selectbox(
     'Which Locatoin?',
     ("長洲", "清水灣", "香港國際機場", "香港天文台", "香港公園", "黃竹坑", "跑馬地", "將軍澳", "九龍城", "京士柏", "滘西洲", "觀塘", "流浮山", "昂坪", "坪洲", "大美督", "啟德跑道公園", "石崗", "沙田", "西貢", "筲箕灣", "上水", "深水埗", "赤柱", "大老山", "打鼓嶺", "大帽山", "大埔", "屯門兒童及青少年院", "荃灣城門谷", "荃灣", "新青衣站", "北潭涌(鯽魚湖)", "山頂", "橫瀾島", "濕地公園", "黃大仙", "元朗公園"))

location_dict = {
 '長洲': 'CCH',
 '清水灣': 'CWB',
 '香港國際機場': 'HKA',
 '香港天文台': 'HKO',
 '香港公園': 'HKP',
 '黃竹坑': 'HKS',
 '跑馬地': 'HPV',
 '將軍澳': 'JKB',
 '九龍城': 'KLT',
 '京士柏': 'KP',
 '滘西洲': 'KSC',
 '觀塘': 'KTG',
 '流浮山': 'LFS',
 '昂坪': 'NGP',
 '坪洲': 'PEN',
 '大美督': 'PLC',
 '啟德跑道公園': 'SE1',
 '石崗': 'SEK',
 '沙田': 'SHA',
 '西貢': 'SKG',
 '筲箕灣': 'SKW',
 '上水': 'SSH',
 '深水埗': 'SSP',
 '赤柱': 'STY',
 '大老山': 'TC',
 '打鼓嶺': 'TKL',
 '大帽山': 'TMS',
 '大埔': 'TPO',
 '屯門兒童及青少年院': 'TU1',
 '荃灣城門谷': 'TW',
 '荃灣': 'TWN',
 '新青衣站': 'TY1',
 '北潭涌(鯽魚湖)': 'TYW',
 '山頂': 'VP1',
 '橫瀾島': 'WGL',
 '濕地公園': 'WLP',
 '黃大仙': 'WTS',
 '元朗公園': 'YLP'
}

st.write('Selected Location : ', location)
st.write('Location Code : ', location_dict[location])

st.write('-'*10)

today = datetime.date.today()
yesterday = today + datetime.timedelta(days=-1)
start_date = st.date_input('Start date', yesterday)
end_date = st.date_input('End date', today)

if start_date > end_date:
    st.error('Error: End date must fall after start date.')






station = location_dict[location]

mean = requests.get(
'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=CLMTEMP&lang=tc&rformat=json&station='
    + station)

low = requests.get(
'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=CLMMINT&lang=tc&rformat=json&station='
    + station)

high = requests.get(
'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=CLMMAXT&lang=tc&rformat=json&station='
    + station)




df_mean = pd.DataFrame(mean.json()['data'] , columns=mean.json()['fields'] )
df_low = pd.DataFrame(low.json()['data'] , columns=low.json()['fields'] )
df_high = pd.DataFrame(high.json()['data'] , columns=high.json()['fields'] )


df_mean["Date"] = df_mean["年/Year"] +'-'+ df_mean["月/Month"] +'-'+ df_mean["日/Day"]
df_mean = df_mean.drop(columns= mean.json()['fields'][4])
df_mean = df_mean.drop(columns= mean.json()['fields'][0:3])
df_mean = df_mean.rename(columns={"數值/Value" : "Average Temperature"})


df_high = df_high.rename(columns={"數值/Value" : "Max Temperature"})
df_high= df_high.drop(columns= high.json()['fields'][4])
df_high = df_high.drop(columns= high.json()['fields'][0:3])


df_low = df_low.rename(columns={"數值/Value" : "Low Temperature"})
df_low= df_low.drop(columns= low.json()['fields'][4])
df_low = df_low.drop(columns= low.json()['fields'][0:3])

df = pd.concat([df_high, df_mean, df_low], axis=1)

#df.columns.tolist()
df = df[['Date','Low Temperature', 'Average Temperature', 'Max Temperature']]

df['Low Temperature'] = pd.to_numeric(df['Low Temperature'], errors='coerce')
df['Average Temperature'] = pd.to_numeric(df['Average Temperature'], errors='coerce')
df['Max Temperature'] = pd.to_numeric(df['Max Temperature'], errors='coerce')

df['Date'] = pd.to_datetime(df['Date'])

df = df.loc[df["Date"].between(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))]



df = df.rename(columns={'Date':'index'}).set_index('index')







st.header('Display Dataframe')
st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')


st.dataframe(df.style.format("{:.1f}"), height=800)



st.write('-'*10)
st.header('Display Line Chart')




st.line_chart(df, use_container_width=True)

st.header('Max Temperature')
st.line_chart(df['Max Temperature'], use_container_width=True)

st.header('Average Temperature')
st.line_chart(df['Average Temperature'], use_container_width=True)

st.header('Low Temperature')
st.line_chart(df['Low Temperature'] , use_container_width=True)





