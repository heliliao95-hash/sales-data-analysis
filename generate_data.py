import pandas as pd
import random

random.seed(42)
products = {"珍珠奶茶": 12, "杨枝甘露": 18, "柠檬茶": 10, "芋泥波波": 16, "四季春茶": 9}
stores = ["A店", "B店", "C店"]
dates = pd.date_range("2026-10-01", "2026-10-31")

for store in stores:
	rows = []
	for _ in range(170):
		d = random.choice(dates)
		p = random.choice(list(products))
		q = random.randint(1, 5)
		rows.append([d.strftime("%Y-%m-%d"), p, q, products[p] * q, store])
	df = pd.DataFrame(rows, columns=["日期", "商品", "数量", "金额", "门店"])

	df = pd.concat([df, df.sample(10, random_state=1)]).reset_index(drop=True)
	df["金额"] = df["金额"].astype(object)
	i1 = df.sample(15, random_state=2).index
	df.loc[i1, "金额"] = df.loc[i1, "金额"].astype(str) + "元"
	i2 = df.sample(8, random_state=3).index
	df.loc[i2, "数量"] = None
	i3 = df.sample(12, random_state=4).index
	df.loc[i3, "日期"] = pd.to_datetime(df.loc[i3, "日期"]).dt.strftime("%Y/%m/%d")

	df.to_csv(f"{store}_销售.csv", index=False, encoding="utf-8-sig")

print("完成")
