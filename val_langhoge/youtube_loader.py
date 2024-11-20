"""
PENDING:
- youtubeloaderが見つからない
- langchain-communityを poetry add で追加しようと思ったけど、langchainとバージョン不整合になる
"""

from langchain.document_loaders import YoutubeLoader

# YouTubeローダーのインスタンスを作成
# language="ja"を指定して日本語の字幕を取得
loader = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    add_video_info=True,  # 動画のメタデータも取得
    language="ja"  # 日本語字幕を指定
)

# 字幕データを読み込む
documents = loader.load()

# 取得したデータを処理
for doc in documents:
    print("=== コンテンツ ===")
    print(doc.page_content)
    print("\n=== メタデータ ===")
    print(doc.metadata)