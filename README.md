! pip3 install paramiko psycopg2
! pip3 install psycopg2-binary

! /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
! brew install postgresql


パッケージインストール
pip3 install -r requirements.txt

# DB立ち上げ （データINSERT）

```
$ docker-compose up -d
```

DBからスキーマデータをdb_schema.jsonに出力

```
$ python3 src/output_db_schema.py
```

実行例
```
$ python3 src/main.py 各学部の学生所属数を教えて
```