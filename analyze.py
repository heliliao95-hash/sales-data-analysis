import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("清洗后_销售数据.csv", parse_dates=["日期"])

# 统计
store = df.groupby("门店")["金额"].sum()
product = df.groupby("商品")["金额"].sum().sort_values(ascending=False)
daily = df.groupby("日期")["金额"].sum()

# 周末 vs 工作日（日均销售额）
daily_df = daily.reset_index()
daily_df["周末"] = daily_df["日期"].dt.dayofweek >= 5
avg = daily_df.groupby("周末")["金额"].mean()

print("各门店销售额：")
print(store)
print("\n商品销售额排名：")
print(product)
print(f"\n工作日日均：{avg[False]:.0f} 元，周末日均：{avg[True]:.0f} 元")
print(f"周末比工作日{'高' if avg[True] > avg[False] else '低'} {abs(avg[True] / avg[False] - 1) * 100:.1f}%")

# 图1：门店销售额
plt.figure(figsize=(6, 4))
store.plot(kind="bar", color="#4C78A8")
plt.title("各门店10月销售额（示例数据）")
plt.ylabel("元")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("图1_门店销售额.png", dpi=150)

# 图2：商品占比
plt.figure(figsize=(6, 6))
product.plot(kind="pie", autopct="%.1f%%")
plt.title("商品销售额占比（示例数据）")
plt.ylabel("")
plt.tight_layout()
plt.savefig("图2_商品占比.png", dpi=150)

# 图3：每日趋势
plt.figure(figsize=(9, 4))
daily.plot(color="#E45756")
plt.title("10月每日销售额趋势（示例数据）")
plt.ylabel("元")
plt.tight_layout()
plt.savefig("图3_每日趋势.png", dpi=150)

print("\n3张图已保存")
