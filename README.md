# End-to-End E-commerce Analytics Platform

## Customer Segmentation and Lifetime Value Prediction
This repository contains the complete source code and documentation for an end-to-end data analytics project. The platform ingests raw e-commerce data, transforms it using a modern data stack, applies machine learning for customer segmentation, and visualizes the results in an interactive executive dashboard.

!(images/dashboard_overview.png)

(https://your-looker-studio-link.com)

### Table of Contents
- (# business-problem)
- (# tech-stack--architecture)
- (# key-insights--business-impact)
- (# data-source)
- (# repository-structure)
- (# setup-and-installation)

License

Contact

### Business Problem
A fictional e-commerce company, "Olist," struggles with an undifferentiated marketing strategy. Their "one-size-fits-all" approach leads to inefficient budget allocation, customer churn, and missed revenue opportunities. The marketing team lacks the tools to identify high-value customers, understand their behavior, or proactively engage users at risk of churning.

This project solves that problem by building a scalable analytics platform that provides a 360-degree view of the customer. The goal is to empower the business to:

+ Optimize Marketing Spend by targeting high-value customer segments.

+ Increase Customer Retention through personalized, data-driven campaigns.

+ Enhance Product Offerings based on the preferences of the most valuable customers.

### Tech Stack & Architecture
This project utilizes a modern ELT (Extract, Load, Transform) paradigm, leveraging the power of a cloud data warehouse to handle transformations in place.

Technologies Used
+ Data Warehouse: Google BigQuery

+ Data Transformation: dbt (Data Build Tool)

+ Machine Learning & Analytics: Python (Pandas, Scikit-learn)

+ Business Intelligence & Visualization: Google Looker Studio

**Architecture Diagram**
The data flows through a simple, robust pipeline:

!(images/architecture.png)

+ Ingestion: Raw CSV data is loaded into Google BigQuery, serving as our single source of truth.

+ Transformation: dbt connects to BigQuery to clean, test, and transform the raw data into a clean, analytics-ready star schema (fact and dimension tables). All business logic is centrally defined in dbt models.

+ Intelligence: A Python script, running in a Jupyter Notebook, queries the transformed data from BigQuery to train a K-Means clustering model for customer segmentation. The results (segment labels) are written back to BigQuery.

+ Presentation: Looker Studio connects directly to the dbt models and the customer segment tables in BigQuery to provide an interactive, shareable dashboard for business stakeholders.

**Key Insights & Business Impact**
The K-Means clustering model successfully segmented customers into five distinct, actionable personas based on their Recency, Frequency, and Monetary (RFM) behavior.

Segment Name	Key Characteristics (Avg. RFM)	Description & Business Strategy
Champions	High R, High F, High M	Best customers. Recently purchased, buy often, and spend the most. Reward them with loyalty programs and early access.
Loyal Customers	Med R, High F, Med M	Frequent shoppers who spend a good amount but may not have purchased recently. Re-engage with personalized promotions.
At-Risk	Low R, Med F, Med M	Good customers who haven't purchased in a long time and are slipping away. Target with win-back campaigns.
New Customers	High R, Low F, Low M	Recent shoppers with low purchase frequency. Nurture them with onboarding campaigns to encourage repeat purchases.
Hibernating	Low R, Low F, Low M	Last purchase was long ago, with low frequency and spend. May not be worth significant marketing investment.

This segmentation allows the business to move from guesswork to data-driven strategy, directly impacting ROI by focusing resources on the most valuable customer groups.    

## Data Source
This project uses the Brazilian E-commerce Public Dataset by Olist, which is publicly available on Kaggle. It contains information on 100,000 orders from 2016 to 2018 made at multiple marketplaces in Brazil.

**Dataset:**(https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Repository Structure
The project is organized to separate the different stages of the data pipeline, following industry best practices.
.
├── dbt_project/              # Contains all dbt models, tests, and configurations
│   ├── models/
│   │   ├── staging/          # 1-to-1 mapping with source tables, light cleaning
│   │   └── marts/            # Final, user-facing fact and dimension tables
│   └── dbt_project.yml       # dbt project configuration file
│
├── notebooks/                # Jupyter Notebook for ML modeling
│   └── customer_segmentation.ipynb
│
├── images/                   # Screenshots and diagrams for the README
│   ├── dashboard_overview.png
│   └── architecture.png
│
├──.gitignore                # Specifies files for Git to ignore (e.g., credentials)
│
└── README.md                 # This file!


## Setup and Installation

To reproduce this project, you will need a Google Cloud Platform account and Python installed locally. Follow these steps:

**1. Google Cloud Platform (GCP) & BigQuery Setup**
   - Create a new project in the [GCP Console](https://console.cloud.google.com/).
   - Enable the **BigQuery API**.
   - Create a **Service Account** with "BigQuery Data Editor" and "BigQuery Job User" roles. Download the JSON key file. **IMPORTANT:** Do not commit this key to GitHub.
   - In BigQuery, create a dataset named `raw_olist_ecommerce`.
   - Upload the Olist CSV files from Kaggle into this dataset.

**2. dbt (Data Build Tool) Setup**
   - Install dbt: `pip install dbt-bigquery`
   - Navigate to the `dbt_project/` directory.
   - Configure your `profiles.yml` file to connect to your BigQuery project using the service account key you downloaded. (dbt provides instructions for this).
   - Run the dbt models:
     ```bash
     dbt deps  # Install dependencies
     dbt run   # Execute all models
     dbt test  # Run data quality tests
     ```

**3. Python & Jupyter Notebook Setup**
   - Install the required Python libraries:
     ```bash
     pip install pandas google-cloud-bigquery pandas-gbq scikit-learn
     ```
   - Open the `notebooks/customer_segmentation.ipynb` file.
   - Update the placeholder variables at the top of the notebook with your GCP `project_id` and the path to your service account JSON key.
   - Run all cells in the notebook to perform customer segmentation and write the results back to BigQuery.

**4. Looker Studio Visualization**
   - Go to(https://lookerstudio.google.com/).
   - Create a new report and add a new data source, selecting the **BigQuery** connector.
   - Connect to the tables created by dbt in your `analytics` dataset (e.g., `fct_orders`, `dim_customers`) and the `customer_segments` table created by the Python script.
   - Build your visualizations and dashboard.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
+ My Name – – chandrima.hazra2003@gmail.com
+ Project Link: https://github.com/chandrimaa3/ecommerce-customer-analytics-platform
