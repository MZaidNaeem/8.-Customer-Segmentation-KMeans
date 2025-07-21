# app.py
import streamlit as st
import pandas as pd
import joblib

# Load pre-trained models
scaler = joblib.load('scaler.pkl')
kmeans = joblib.load('custumer_clustering.pkl')

# Mapping cluster numbers to business labels
cluster_mapping = {
    0: "RETAIN",
    1: "RE-ENGAGE",
    2: "NURTURE",
    3: "REWARD",
    -1: "PAMPER",
    -2: "UPSELL",
    -3: "DELIGHT"
}

# Streamlit UI
st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🧠 Customer Segmentation App")
st.write("Upload your customer dataset to get segment labels using K-Means clustering.")

uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Uploaded Data (Preview)")
        st.dataframe(df, height=300)

        # Check required columns
        required_cols = ["MonetaryValue", "Frequency", "Recency"]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
        else:
            # Scale the data
            scaled_input = scaler.transform(df[required_cols])

            # Predict clusters
            clusters = kmeans.predict(scaled_input)

            # Map clusters to business labels
            df["Cluster"] = clusters
            df["Segment"] = df["Cluster"].map(cluster_mapping).fillna("UNDEFINED")


            st.subheader("📊 Full Segmented Data (Preview)")
            st.dataframe(
                df[["MonetaryValue", "Frequency", "Recency", "Segment"]],
                height=500
            )

            # Download segmented data
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Segmented Data",
                data=csv,
                file_name="segmented_customers.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error("❗ An error occurred while processing your file.")
        st.text(str(e))
else:
    st.info("ℹ️ Please upload a CSV file with columns: MonetaryValue, Frequency, Recency.")
