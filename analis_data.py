import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class DataLoader:
    def __init__ (self, filepath):
        self.filepath = filepath

    def load(self):
        df = pd.read_csv(self.filepath, low_memory=False)
        return df

class DataCleaner:
    def __init__ (self, df):
        self.df = df

    def clean (self):
        self.df = self.df.drop(columns=["Unnamed: 22"]) 
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        return self.df

class DataAnalyze:
    def __init__ (self, df):
        self.df = df

    def pendapatan_per_bulan(self):
        return self.df.groupby(self.df["Date"].dt.to_period("M"))["Amount"].sum()

    def produk_terlaris(self):
        return self.df.groupby("Category")["Qty"].sum().sort_values(ascending=False)

    def produk_per_bulan(self):
        return self.df.groupby([self.df["Date"].dt.to_period("M"), "Category"])["Qty"].sum()

class DataVisualizer:
    def __init__ (self, analyzer):
        self.analyzer = analyzer

    def grafik_pendapatan(self):
        data = self.analyzer.pendapatan_per_bulan()
        data.plot(kind = "bar")
        plt.title("Pendapatan per Bulan")
        plt.xlabel("Bulan")
        plt.ylabel("Total Pendapatan (INR)")
        plt.tight_layout()
        st.pyplot(plt)

    def produk_terlaris(self):
        data = self.analyzer.produk_terlaris()
        fig, ax = plt.subplots()
        ax.pie(data, labels=data.index, wedgeprops=dict(width=0.5))
        ax.legend(data.index, loc="best")
        plt.title("Produk Terlaris")
        plt.tight_layout()
        st.pyplot(plt)

    def produk_per_bulan(self):
        data = self.analyzer.produk_per_bulan()
        data = data.reset_index()

        data ["Date"] = data ["Date"].astype(str)

        bulan_pilihan = st.selectbox(
            "Pilih Bulan:", 
            options=data["Date"].unique()
        )

        data_filter = data[data["Date"] == bulan_pilihan] 
        fig, ax = plt.subplots()
        ax.bar(data_filter["Category"], data_filter ["Qty"])
        ax.set_title(f"Produk Terjual - Bulan {bulan_pilihan}")
        ax.set_xlabel("kategori")
        ax.set_ylabel("Jumlah terjual")
        plt.tight_layout()
        st.pyplot(fig)

loader = DataLoader("Amazon Sale Report.csv")
df = loader.load()

cleaner = DataCleaner(df)
df_clean = cleaner.clean()

analyzer = DataAnalyze(df_clean)
st.title("Dashboard Penjualan Amazon di India ")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", "INR 78.5 Juta")
col2.metric("Produk Terlaris", "Set")
col3.metric("Bulan Terbaik", "April 2022")

visualizer = DataVisualizer(analyzer)
visualizer.grafik_pendapatan()
visualizer.produk_terlaris()
visualizer.produk_per_bulan()
