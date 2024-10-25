from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import datetime
import requests


PROMPT = """
<CurrentTime>
{time_stamp}
</CurrentTime>

<Location>
<Latitude>
{latitude}
</Latitude>

<Longitude>
{longitude}
</Longitude>
</Location>

<Question>
{question}
</Question>
"""


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーを環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")



geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
data = requests.get(geo_request_url).json()
print(data['latitude'])
print(data['longitude'])


# タイムスタンプを取得
time_stamp = datetime.datetime.now()
time_stamp = str(time_stamp)


# 質問を設定
question = "今日以降で最も近い祝日はいつですか？"

# ChatGPT-4モデルのインスタンスを作成
model = ChatOpenAI(model_name="gpt-4o", api_key=api_key)

# プロンプトテンプレートを定義
prompt = ChatPromptTemplate.from_template(PROMPT)
formatted_prompt = prompt.format(question=question, time_stamp=time_stamp, latitude=data["latitude"], longitude=data["longitude"])

print("--------formatted_prompt---------")
print(formatted_prompt)
print("---------------------------------")

# LLMChainを作成
answer = model.invoke(formatted_prompt)

print(answer)
