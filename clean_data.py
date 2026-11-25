import pandas as pd

# 1. 读取并合并三家门店
files = ["A店_销售.csv", "B店_销售.csv", "C店_销售.csv"]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print("合并后行数：", len(df))
print("清洗前各列空值：")
print(df.isna().sum())

# 2. 金额：去掉“元”，转成数字
df["金额"] = df["金额"].astype(str).str.replace("元", "", regex=False).astype(float)

# 3. 日期：统一格式
df["日期"] = pd.to_datetime(df["日期"], format="mixed")

# 4. 数量缺失：用“金额 ÷ 该商品单价”推算回来
df["单价"] = df["金额"] / df["数量"]
price = df.groupby("商品")["单价"].median()
mask = df["数量"].isna()
df.loc[mask, "数量"] = (df.loc[mask, "金额"] / df.loc[mask, "商品"].map(price)).round()
df = df.drop(columns="单价")

# 5. 去重
before = len(df)
df = df.drop_duplicates()
print("去掉重复行：", before - len(df))

# 6. 保存
df = df.sort_values(["日期", "门店"]).reset_index(drop=True)
df.to_csv("清洗后_销售数据.csv", index=False, encoding="utf-8-sig")
print("清洗后行数：", len(df))
print("清洗后各列空值：")
print(df.isna().sum())
