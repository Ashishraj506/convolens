import re
import pandas as pd

# Read chat file
with open("sample_chat.txt", "r", encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Normalize special Unicode spaces
data = data.replace('\u202f', ' ').replace('\u00a0', ' ')

# Pattern to match timestamps
pattern = r'(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm))\s-\s'

# Extract timestamps
dates = re.findall(pattern, data)

# Split messages
messages = re.split(pattern, data)[2:]

users = []
texts = []

for msg in messages:
    parts = msg.split(': ', 1)

    if len(parts) == 2:
        users.append(parts[0].strip())
        texts.append(parts[1].strip())
    else:
        users.append("group_notification")
        texts.append(msg.strip())

# Ensure equal lengths
n = min(len(dates), len(users), len(texts))

# Create DataFrame
df = pd.DataFrame({
    'date': dates[:n],
    'user': users[:n],
    'message': texts[:n]
})

# Display result
print("Total messages:", len(df))
print()
# ---------------- BASIC STATISTICS ----------------

# Total messages
total_messages = df.shape[0]

# Total users (excluding group notifications)
total_users = df[df['user'] != 'group_notification']['user'].nunique()

# Total words
total_words = df['message'].apply(lambda x: len(str(x).split())).sum()

print("\n===== BASIC STATISTICS =====")
print("Total Messages:", total_messages)
print("Total Users:", total_users)
print("Total Words:", total_words)

# Top 10 most active users
print("\n===== TOP 10 ACTIVE USERS =====")
print(df['user'].value_counts().head(10))

import matplotlib.pyplot as plt

# Get top 10 users
top_users = df['user'].value_counts().head(10)

# Create bar chart
plt.figure(figsize=(10, 6))
top_users.plot(kind='bar')

# Add title and labels
plt.title("Top 10 Active Users")
plt.xlabel("Users")
plt.ylabel("Number of Messages")

# Improve layout
plt.xticks(rotation=45)
plt.tight_layout()

# Show chart
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Combine all messages into one string
text = ' '.join(df['message'].astype(str))

# Create word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white'
).generate(text)

# Display word cloud
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Words in Chat")
plt.show()

# Convert date column to datetime
df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p', errors='coerce')

# Extract only the date part
df['only_date'] = df['datetime'].dt.date

# Count messages per day
daily_messages = df.groupby('only_date').size()

# Plot daily trend
plt.figure(figsize=(12, 6))
daily_messages.plot(kind='line', marker='o')

plt.title("Daily Message Trend")
plt.xlabel("Date")
plt.ylabel("Number of Messages")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
