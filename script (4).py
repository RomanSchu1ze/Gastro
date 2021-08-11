#!/usr/bin/env python
# coding: utf-8

# ### Gastro Hochlauf DB Fernverkehr

# In[449]:


# Bibliotheken
import pandas as pd
import numpy as np


# In[450]:


# Bereinigung der Daten
def clean_data(df):
    df.replace("*", np.nan, inplace=True)
    for col in df.columns:
        if col not in ["Datum", "Kreis", "Berufe ID"]:
            df[col] = df[col].astype("float64")
    return df


# ##### 1. Beschäftigte

# In[451]:


# Daten einlesen
colnames=["Datum", "Kreis", "Berufe ID", "SvB", "agB"]
df = pd.read_csv("Daten/202009_Besch_Kreise.csv", names=colnames, header=None, sep=";", index_col=False)


# In[452]:


# Daten bereinigen
df = clean_data(df)


# In[453]:


# erste fünf Zeilen
df.head()


# In[454]:


# relevante Berufe ID´s
Berufe = [2, 50, 78, 79]


# In[455]:


# relevante Regionen mit zugehörigen Kreisschlüsseln
Regionen = {"Berlin":[11000, 12054],
            "Frankfurt":[6411, 6412, 6413, 6414, 6432, 6433, 6434, 6436, 6438, 6440],
            "München":[9162,9188, 9174, 9175, 9177, 9178, 9179, 9182, 9184, 9188],
            "Hamburg":[1053, 1056, 1062, 2000, 3353],
            "Köln":[5314, 5315, 5316, 5358, 5362, 5366, 5374, 5378, 5382],
            "Dortmund":[5512, 5513, 5562, 5911, 5913, 5914, 5915, 5916, 5954, 5962, 5974, 5978],
            "Münster":[5515, 5558, 5566, 5570],
            "Leipzig":[14713, 14729, 14730, 15002, 15088],
            "Kassel":[3159, 6611, 6633, 6634, 6636],
            "Hannover":[3157, 3241, 3252, 3254, 3256, 3257, 3351],
            "Mainz":[7315, 7339, 9661, 9671],
            "Nürnberg":[9373, 9474, 9561, 9562, 9563, 9564, 9565, 9571, 9572, 9573, 9574, 9575, 9576],
            "Mannheim":[6431, 7311, 7314, 7316, 7318, 7332, 7338, 8221, 8226],
            "Karlsruhe":[7313, 7334, 7337, 8211, 8212, 8215, 8216],
            "Stuttgart":[8111, 8115, 8116, 8117, 8118, 8119, 8121, 8125, 8231, 8235, 8236, 8415, 8416]
           }


# In[456]:


# Daten ziehen
def get_data():
    list_of_df = []
    for key, value in Regionen.items():
        df_sub = df[df.Kreis.isin(value)]
        df_sub = df_sub.copy()
        df_sub.loc[:, "Region"] = key
        df_sub = df_sub[df_sub["Berufe ID"].isin(Berufe)]
        df_sub.loc[df_sub["Berufe ID"] == 2, "Beruf"] = "Fachkräfte"
        df_sub.loc[df_sub["Berufe ID"] == 50, "Beruf"] = "Verkaufsberufe"
        df_sub.loc[df_sub["Berufe ID"] == 78, "Beruf"] = "Hotellerie"
        df_sub.loc[df_sub["Berufe ID"] == 79, "Beruf"] = "Gastronomie"
        list_of_df.append(df_sub)
    df_emp = pd.concat(list_of_df)
    return df_emp


# In[457]:


# relevante Zeilen extrahieren
df_emp = get_data()


# In[458]:


# Relevante Spalten behalten und umsortieren
columns = ["Kreis", "Region", "Berufe ID", "Beruf", "SvB", "agB"]
df_emp = df_emp[columns]


# In[459]:


# erste fünf Zeilen
df_emp.head()


# In[460]:


# Aggregierte Daten ausgeben
# df_emp.groupby(["Region","Beruf"]).SvB.sum()


# ##### 2. Arbeitslose

# In[463]:


# Daten einlesen
colnames=["Datum", "Kreis", "Berufe ID", "Alo"]
df = pd.read_csv("Daten/202009_ALO_Kreise.csv", names=colnames, header=None, sep=";", index_col=False)


# In[464]:


# Daten bereinigen
df = clean_data(df)


# In[465]:


# erste fünf Zeilen
df.tail()


# In[466]:


# Anpassung der Datenspalte Kreise, sodass identisch mit Beschäftigtendaten
def format_Kreise():
    df["mask"] = [len(str(item)) for item in df["Kreis"]]
    df.loc[df["mask"] == 7, "Kreis"] = pd.to_numeric(df.loc[df["mask"] == 7, "Kreis"].astype(str).str[:4], errors="coerce")
    df.loc[df["mask"] == 8, "Kreis"] = pd.to_numeric(df.loc[df["mask"] == 8, "Kreis"].astype(str).str[:5], errors="coerce")
    df_sub = df.drop(labels="mask", axis=1)
    return df_sub


# In[467]:


# Daten formattieren
df = format_Kreise()


# In[468]:


# Datentypen prüfen
df.dtypes


# In[469]:


# relevante Zeilen extrahieren
df_alo = get_data()


# In[470]:


# Relevante Spalten behalten und umsortieren
columns = ["Kreis", "Region", "Berufe ID", "Beruf", "Alo"]
df_alo = df_alo[columns]


# ##### 3. Stellenausschreibungen

# In[471]:


# Daten einlesen
colnames=["Datum", "Kreis", "Berufe ID", "Stellen"]
df = pd.read_csv("Daten/202009_SteA.csv", names=colnames, header=None, sep=";", index_col=False)


# In[472]:


# erste fünf Zeilen
df.head()


# In[473]:


# Daten bereinigen
df = clean_data(df)


# In[474]:


# Daten formattieren
df = format_Kreise()


# In[475]:


# Datentypen
df.dtypes


# In[476]:


# relevante Daten extrahieren
df_stellen = get_data()


# In[477]:


# Spalten sortieren
columns = ["Kreis", "Region", "Berufe ID", "Beruf", "Stellen"]
df_stellen = df_stellen[columns]


# In[478]:


# erste fünf Zeilen
df_stellen.head()


# In[479]:


# Format der Daten 
print(df_alo.shape, df_emp.shape, df_stellen.shape)


# ##### 4. Merge der Daten

# In[ ]:


# Merge von Arbeitslosen, gem. Stellen und Beschäftigten
result = df_emp.merge(df_alo.merge(df_stellen, how="left", on=["Region", "Beruf", "Kreis", "Berufe ID"]), 
                      how="left", on=["Region", "Beruf", "Kreis", "Berufe ID"])


# In[481]:


# Format des finalen Dataframes
result.shape


# In[482]:


# als Excel speichern
result.to_excel("Daten_Boardserice.xlsx")


# In[483]:


# erste fünf Zeilen 
result.head()


# In[ ]:




