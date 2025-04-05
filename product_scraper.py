import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Request the Website Data
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract Product Info
products = soup.find_all("article", class_="product_pod")

titles = []
prices = []
ratings = []

for product in products:
    title = product.h3.a["title"]
    price = float(product.select_one(".price_color").text.replace("£", ""))
    rating_str = product.p["class"][1]
    rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}[rating_str]

    titles.append(title)
    prices.append(price)
    ratings.append(rating)

# Step 3: Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Rating": ratings
})

# Save to CSV
df.to_csv("products.csv", index=False)

# Step 4: Data Analysis
avg_price = df["Price"].mean()
print(f"Average product price: £{avg_price:.2f}")

# Step 5: Visualizations
sns.set(style="whitegrid")

# Price Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["Price"], bins=10, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("price_dist.png")
plt.close()

# Rating Distribution
plt.figure(figsize=(8, 5))
sns.countplot(x="Rating", data=df)
plt.title("Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("rating_dist.png")
plt.close()

# Price by Rating
plt.figure(figsize=(8, 5))
sns.boxplot(x="Rating", y="Price", data=df)
plt.title("Price by Rating")
plt.xlabel("Rating")
plt.ylabel("Price (£)")
plt.tight_layout()
plt.savefig("price_by_rating.png")
plt.close()
