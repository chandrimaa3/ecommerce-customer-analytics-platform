import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from google.cloud import bigquery
from google.oauth2 import service_account

# --- 1. Connect to BigQuery and Load Data ---
creds = service_account.Credentials.from_service_account_file('/home/chandrima_hazra2003/scenic-index-474117-f8-50087d844632.json')
project_id = 'scenic-index-474117-f8'
sql_query = "SELECT * FROM `scenic-index-474117-f8.analytics.dim_customers`"

df_customers = pd.read_gbq(sql_query, project_id=project_id, credentials=creds)

# --- 2. Feature Engineering (RFM) ---
snapshot_date = df_customers['most_recent_order_date'].max() + pd.Timedelta(days=1)
df_rfm = df_customers.groupby('customer_unique_id').agg({
    'most_recent_order_date': lambda date: (snapshot_date - date.max()).days
}).rename(columns={'most_recent_order_date': 'Recency'})

# For Monetary, we need to join with fct_orders
sql_orders = "SELECT * FROM `scenic-index-474117-f8.analytics.fct_orders`"
df_orders = pd.read_gbq(sql_orders, project_id=project_id, credentials=creds)

# Merge customer and order data
df_customers_merged = pd.merge(df_customers, df_orders, on='customer_id', how='left')

# Calculate Frequency and Monetary value
df_freq_monetary = df_customers_merged.groupby('customer_unique_id').agg(Frequency=('order_id', 'nunique'), Monetary=('payment_value', 'sum')).reset_index()

df_rfm = pd.merge(df_rfm, df_freq_monetary, on='customer_unique_id')

# --- 3. Preprocessing and Clustering ---
rfm_features = df_rfm[['Recency', 'Frequency', 'Monetary']]
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)

kmeans = KMeans(n_clusters=5, random_state=42)
df_rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# --- 4. Create Dataset and Write Results back to BigQuery ---
client = bigquery.Client(credentials=creds, project=project_id)
dataset_id = f"{project_id}.analytics"

try:
    client.get_dataset(dataset_id)
except Exception:
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    client.create_dataset(dataset, timeout=30)

df_rfm.to_gbq(
    'analytics.customer_segments',
    project_id=project_id,
    credentials=creds,
    if_exists='replace',
    location='US'
)
print("Customer segments written to BigQuery.")