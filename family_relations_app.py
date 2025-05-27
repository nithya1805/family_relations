import streamlit as st
import pandas as pd

# Relationship data
data = [
    {"English": "Mother", "Hindi": "माता / माँ"},
    {"English": "Father", "Hindi": "पिता / पापा"},
    {"English": "Son", "Hindi": "बेटा / पुत्र"},
    {"English": "Daughter", "Hindi": "बेटी / पुत्री"},
    {"English": "Brother", "Hindi": "भाई"},
    {"English": "Sister", "Hindi": "बहन"},
    {"English": "Paternal Grandfather", "Hindi": "दादा / बाबा"},
    {"English": "Paternal Grandmother", "Hindi": "दादी"},
    {"English": "Maternal Grandfather", "Hindi": "नाना"},
    {"English": "Maternal Grandmother", "Hindi": "नानी"},
    {"English": "Paternal Uncle (Father’s Brother)", "Hindi": "चाचा"},
    {"English": "Paternal Aunt (Uncle’s Wife)", "Hindi": "चाची"},
    {"English": "Maternal Uncle (Mother’s Brother)", "Hindi": "मामा"},
    {"English": "Maternal Aunt (Uncle’s Wife)", "Hindi": "मामी"},
    {"English": "Father’s Sister", "Hindi": "बुआ"},
    {"English": "Father's Sister's Husband", "Hindi": "फूफा"},
    {"English": "Mother's Sister", "Hindi": "मौसी"},
    {"English": "Mother's Sister's Husband", "Hindi": "मौसा"},
    {"English": "Father-in-law", "Hindi": "ससुर"},
    {"English": "Mother-in-law", "Hindi": "सास"},
    {"English": "Son-in-law", "Hindi": "दामाद"},
    {"English": "Daughter-in-law", "Hindi": "बहू"},
    {"English": "Brother-in-law (Wife’s Brother)", "Hindi": "साला"},
    {"English": "Sister-in-law (Wife’s Sister)", "Hindi": "साली"},
    {"English": "Sister-in-law (Brother’s Wife)", "Hindi": "भाभी"},
    {"English": "Grandson (Son’s child)", "Hindi": "पोता"},
    {"English": "Granddaughter (Son’s child)", "Hindi": "पोती"},
    {"English": "Grandson (Daughter’s child)", "Hindi": "नाती"},
    {"English": "Granddaughter (Daughter’s child)", "Hindi": "नातिनी"},
    {"English": "Nephew (Brother’s Son)", "Hindi": "भतीजा"},
    {"English": "Niece (Brother’s Daughter)", "Hindi": "भतीजी"},
    {"English": "Nephew (Sister’s Son)", "Hindi": "भांजा / भानेज"},
    {"English": "Niece (Sister’s Daughter)", "Hindi": "भांजी"},
    {"English": "Step Brother", "Hindi": "सौतेला भाई"},
    {"English": "Step Sister", "Hindi": "सौतेली बहन"},
    {"English": "Step Father", "Hindi": "सौतेला पिता"},
    {"English": "Step Mother", "Hindi": "सौतेली माँ"},
    {"English": "Adopted Son", "Hindi": "गोद लिया बेटा"},
    {"English": "Adopted Daughter", "Hindi": "गोद ली हुई बेटी"},
    {"English": "Cousin Brother (Paternal Uncle's Son)", "Hindi": "चचेरा भाई"},
    {"English": "Cousin Sister (Paternal Uncle's Daughter)", "Hindi": "चचेरी बहन"},
    {"English": "Cousin Brother (Maternal Uncle's Son)", "Hindi": "ममेरा भाई"},
    {"English": "Cousin Sister (Maternal Uncle's Daughter)", "Hindi": "ममेरी बहन"},
    {"English": "Cousin Brother (Father's Sister's Son)", "Hindi": "फुफेरा भाई"},
    {"English": "Cousin Sister (Father's Sister's Daughter)", "Hindi": "फुफेरी बहन"},
    {"English": "Cousin Brother (Mother's Sister's Son)", "Hindi": "मौसेरा भाई"},
    {"English": "Cousin Sister (Mother's Sister's Daughter)", "Hindi": "मौसेरी बहन"},
    {"English": "Brother-in-law (Sister's Husband)", "Hindi": "बहनोई"},
    {"English": "Wife", "Hindi": "पत्नी"},
    {"English": "Husband of wife's sister", "Hindi": "साढ़ू भाई"},
    {"English": "Elder brother-in-law", "Hindi": "जेठ"},
    {"English": "Younger brother-in-law", "Hindi": "देवर"},
    {"English": "Great-grandfather", "Hindi": "परदादा / परआजा"},
    {"English": "Father’s elder brother", "Hindi": "ताऊ"},
    {"English": "Father’s elder brother’s wife", "Hindi": "ताई"},
    {"English": "Younger brother's wife", "Hindi": "नथी"},
    {"English": "Paternal aunt’s daughter", "Hindi": "फुफैली"},
    {"English": "Great-grandchild", "Hindi": "परआजा"},
    {"English": "Wife of your husband's brother", "Hindi": "सरहज"},
]

# Convert to DataFrame
df = pd.DataFrame(data)

st.title("👨‍👩‍👧‍👦 Family Relationship Finder")

# Search input
search = st.text_input("🔍 Type to search relationship (English or Hindi):")

# Filter results
if search:
    filtered = df[df.apply(lambda row: search.lower() in row['English'].lower() or search in row['Hindi'], axis=1)]
    st.table(filtered)
else:
    st.table(df)
