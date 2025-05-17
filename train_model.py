import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

df = pd.read_csv(
    r'C:\Users\Harshini K\Downloads\archive (4)\data.csv',
    encoding='latin1',
    delimiter=';',
    on_bad_lines='skip'
)
print(df["KTAS_RN"].value_counts())
print(df.columns)

# Remove "Chief_complain" from features
features = ["Age", "HR", "BT", "Saturation"]
X = df[features].replace('??', pd.NA)

# Convert numeric columns to float
for col in ["Age", "HR", "BT", "Saturation"]:
    X[col] = pd.to_numeric(X[col], errors='coerce')

# Drop rows with missing values
X = X.dropna()
y = df.loc[X.index, "KTAS_RN"]

# Convert KTAS_RN to binary: 1/2 = Critical, 3/4/5 = Not Critical
y = y.apply(lambda x: 1 if x in [1, 2] else 0)

print(y.value_counts())

# No one-hot encoding needed since "Chief_complain" is removed

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X, y)

model.feature_names = X.columns.tolist()
model.target_names = ['Not Critical', 'Critical']

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)