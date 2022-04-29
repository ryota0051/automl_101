## これはなにか

AutoMl のお試し

## 使い方

1. `docker-compose build`でイメージ作成

2. `docker-compose up`を実行して、`localhost:8888`にブラウザでアクセス

## デフォルトの特徴量で試す場合

`./notebook/automl_tutorial.ipynb`にて`生データをそのまま学習してみる`以下のセルを実行する。

## EDA などをする場合

`./notebook/eda.ipynb`を使用

## 特徴量抽出した結果で学習する場合

1. `./notebook/feature_generation.ipynb`で学習用の csv ファイルを作成する。

2. `./notebook/automl_tutorial.ipynb`にて`前処理ありデータで学習してみる`以下のセルを実行

## 所感

1. タイタニックデータは、以下のような理由であまり初心者向けではないように感じた。

   - データ数が少ない

   - 同じ家族が train と test にまたがっており、それが割と重要な特徴量となるらしい

     これらの特徴量を上手く使えば、そもそも機械学習を用いなくても割と良い精度がでるよう(例えば、[こちらの例](https://www.kaggle.com/code/jack89roberts/titanic-using-ticket-groupings/notebook))

2. AutoMl について

   - サラッとモデルを試すレベルだと便利だが、細々したところを試そうとすると面倒になる印象

   - 使うタイミング的には、モデル選定時など？
