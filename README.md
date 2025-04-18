詳細は[LangGraphでつくる！プロンプトに応じてDBデータから自由にグラフ画像を生成するAIエージェント](https://zenn.dev/medicalforce/articles/82d2bbbbd711cf)を参照してください。

# Pythonの仮想環境を作成、アクティベート
```
$ python -m venv [仮想環境名]
$ . [仮想環境名]/bin/activate
```

# パッケージインストール
```
$ pip install -r requirements.txt
```

# DB立ち上げ （+初期データINSERT）

```
$ docker-compose up -d
```

DBからスキーマデータをdb_schema.jsonに出力

```
$ python src/output_db_schema.py
```

実行例
```
$ python src/main.py 各学部の学生所属数を教えて
```