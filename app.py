import streamlit as st
import pandas as pd
from pydub.generators import Sine
from pydub import AudioSegment
import tempfile

st.title("CSV → メトロノーム音 Generator")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

tempo_ratio = st.slider("テンポ倍率（%）", min_value=50, max_value=150, value=100, step=5)

if uploaded_file:
	df = pd.read_csv(uploaded_file)
	st.dataframe(df.head())

	tempos = df["テンポ"].tolist()
	拍位置 = df["拍位置"].tolist()
	
	# 音を生成
	accent = Sine(1200).to_audio_segment(duration=70).apply_gain(-3)
	regular = Sine(1000).to_audio_segment(duration=50).apply_gain(-6)
	
	track = AudioSegment.silent(duration=0)
	
	for tempo, beat in zip(tempos, 拍位置):
	    bpm = tempo * (tempo_ratio / 100)
	    interval = 60_000 / bpm
	
	    if ".1." in beat:
	        track += accent + AudioSegment.silent(duration=interval - 70)
	    else:
	        track += regular + AudioSegment.silent(duration=interval - 50)
	
	# 一時ファイルに保存して再生
	with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
	    track.export(tmp.name, format="wav")
	    st.audio(tmp.name)
	
	