from typing import List
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def get_train_and_test_df(train_df, test_df):
    train_df = get_featured_added_df(train_df)
    test_df = get_featured_added_df(test_df)
    train_df, test_df = label_encode(train_df, test_df)
    return train_df, test_df


def get_featured_added_df(df: pd.DataFrame) -> pd.DataFrame:
    fill_null_df(df)
    df['FamilySize'] = get_family_size(df)
    df['BoyOrFemale'] = get_boy_or_female_series(df)
    df['FareBin'] = get_bin_data(df, 'Fare', 5)
    df['AgeBin'] = get_bin_data(df, 'Age', 4)
    df['Title'] = get_name_title(df)
    drop_col_list = ['Cabin', 'Age', 'Fare', 'Name', 'Ticket']
    drop_col(df, drop_col_list)
    return df


def label_encode(
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        target_col_list: List[str] = ['Sex', 'Embarked', 'Title']):
    for target_col in target_col_list:
        le = LabelEncoder()
        le.fit(train_df[target_col])
        train_df[target_col] = le.transform(train_df[target_col])
        test_df[target_col] = le.transform(test_df[target_col])
    return train_df, test_df


def drop_col(df: pd.DataFrame, drop_target_col_list: List[str]):
    df.drop(drop_target_col_list, axis=1, inplace=True)


def get_family_size(df: pd.DataFrame) -> pd.Series:
    """SibSp(兄弟、配偶者数)とParch(親、子供の数)を足し合わせた特徴量を返す
    Args:
        - df: 対象データフレーム

    Returns:
        家族数
    """
    return df['Parch'] + df['SibSp']


def get_bin_data(df: pd.DataFrame, col: str, bins: int) -> pd.Series:
    """AgeやFareをbinningする

    Args:
        - df: 対象データフレーム
        - col: 対象カラム
        - bins: ビンの数

    Returns:
        binning結果
    """
    return pd.qcut(df[col], bins, labels=False)


def fill_null_df(df: pd.DataFrame):
    def fill_null_age():
        title = get_name_title(df)
        unique_title_list = title.unique().tolist()
        for unique_title in unique_title_list:
            target_filter = title == unique_title
            fill_age = df.loc[target_filter, 'Age'].median()
            df.loc[target_filter, 'Age'] = df.loc[target_filter, 'Age'].fillna(fill_age)

    # 年齢の欠損値補完(年齢は、敬称ごとの中央値で埋める)
    fill_null_age()
    # Fare欠損値補完
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    # Embarkedを最瀕値で埋める
    df['Embarked'].fillna(df['Embarked'].value_counts().index[0], inplace=True)


def get_name_title(df: pd.DataFrame) -> pd.Series:
    title = df['Name'].str.extract(r'([A-Za-z]+)\.', expand=False)
    mapping = {'Mlle': 'Miss', 'Ms': 'Miss', 'Mme': 'Mrs'}
    title = title.apply(lambda x: x if mapping.get(x) is None else mapping[x])
    return title.replace(
        ['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'],
        'Uncommon'
    )


def get_boy_or_female_series(df: pd.DataFrame) -> pd.Series:
    """子供か女性かのフラグを返す

    Args:
        df: 対象データフレーム

    Returns:
        0: 女性か子供ではない
        1: 女性もしくは子供
        のシリーズデータ
    """
    # 「Masterが敬称についている」または「10歳以下の男性」
    boy = (
        (df['Name'].str.contains('Master')) | ((df['Sex'] == 'male') & (df['Age'] < 10))
    )
    female = df['Sex'] == 'female'
    boy_or_female = boy | female
    return boy_or_female.apply(lambda x: 0 if x else 1)
