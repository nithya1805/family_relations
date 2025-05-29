import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Family Relationship Finder", layout="centered")
st.title("👨‍👩‍👧‍👦 Family Relationship Finder")

# 📁 CSV file path
CSV_FILE = "family_relationships.csv"

# 🔢 Initial fallback data
initial_data = [
    ["Mother", "माता / माँ"], ["Father", "पिता / पापा"], ["Son", "बेटा / पुत्र"], ["Daughter", "बेटी / पुत्री"],
    ["Brother", "भाई"], ["Sister", "बहन"], ["Paternal Grandfather", "दादा / बाबा"],
    ["Paternal Grandmother", "दादी"], ["Maternal Grandfather", "नाना"], ["Maternal Grandmother", "नानी"],
    ["Paternal Uncle (Father’s Brother)", "चाचा"], ["Paternal Aunt (Uncle’s Wife)", "चाची"],
    ["Maternal Uncle (Mother’s Brother)", "मामा"], ["Maternal Aunt (Uncle’s Wife)", "मामी"],
    ["Father’s Sister", "बुआ"], ["Father's Sister's Husband", "फूफा"], ["Mother's Sister's Husband", "मौसा"],
    ["Mother's Sister", "मौसी"], ["Father-in-law", "ससुर"], ["Mother-in-law", "सास"], ["Son-in-law", "दामाद"],
    ["Daughter-in-law", "बहू"], ["Brother-in-law (Wife’s Brother)", "साला"],
    ["Sister-in-law (Wife’s Sister)", "साली"], ["Sister-in-law (Brother’s Wife)", "भाभी"],
    ["Grandson (Son’s child)", "पोता"], ["Granddaughter (Son’s child)", "पोती"],
    ["Grandson (Daughter’s child)", "नाती"], ["Granddaughter (Daughter’s child)", "नातिनी"],
    ["Nephew (Brother’s Son)", "भतीजा"], ["Niece (Brother’s Daughter)", "भतीजी"],
    ["Nephew (Sister’s Son)", "भांजा / भानेज"], ["Niece (Sister’s Daughter)", "भांजी"],
    ["Step Brother", "सौतेला भाई"], ["Step Sister", "सौतेली बहन"], ["Step Father", "सौतेला पिता"],
    ["Step Mother", "सौतेली माँ"], ["Adopted Son", "गोद लिया बेटा"], ["Adopted Daughter", "गोद ली हुई बेटी"],
    ["Cousin Brother (Paternal Uncle's Son)", "चचेरा भाई"], ["Cousin Sister (Paternal Uncle's Daughter)", "चचेरी बहन"],
    ["Cousin Brother (Maternal Uncle's Son)", "ममेरा भाई"], ["Cousin Sister (Maternal Uncle's Daughter)", "ममेरी बहन"],
    ["Cousin Brother (Father's Sister's Son)", "फुफेरा भाई"], ["Cousin Sister (Father's Sister's Daughter)", "फुफेरी बहन"],
    ["Cousin Brother (Mother's Sister's Son)", "मौसेरा भाई"], ["Cousin Sister (Mother's Sister's Daughter)", "मौसेरी बहन"],
    ["Son of Paternal Cousin Brother", "चचेरा भतीजा"], ["Daughter of Paternal Cousin Brother", "चचेरी भतीजी"],
    ["Son of Paternal Aunt’s Son", "फुफेरा भतीजा"], ["Daughter of Paternal Aunt’s Son", "फुफेरी भतीजी"],
    ["father's sister", "फुवा"], ["Brother-in-law", "जीजा"], ["Wife", "पत्नी"],
    ["Husband of wife’s sister", "साढ़ू भाई"], ["Elder brother in law", "जेठ"], ["younger brother-in-law", "देवर"],
    ["Great-grandfather (father’s father’s father)", "परदादा / परआजा"], ["Father’s elder brother", "ताऊ"],
    ["Father’s elder brother’s wife", "ताई"], ["younger brother's wife (sister-in-law )", "नथी"],
    ["paternal aunt's daughter", "फुफैली"], ["Great-grandchild", "परआजा"], ["Brother-in-law(sister's husband)", "बहनोई"],
    ["wife of your husband's brother", "सरहज"]
]

# 📥 Load or initialize DataFrame
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(initial_data, columns=["English", "Hindi"])

# 💾 Save DataFrame to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# 🔁 Load data into session state if not present
if "relation_df" not in st.session_state:
    st.session_state.relation_df = load_data()

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []

df = st.session_state.relation_df

# 🔍 Search
search = st.text_input("🔍 Search relationship (English or Hindi):")
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: search.lower() in row["English"].lower() or search.lower() in row["Hindi"].lower(),
            axis=1
        )
    ]

st.table(filtered_df)

st.markdown("---")

# ✏️ Edit Relationship
st.subheader("✏️ Edit Existing Relationship")
relation_options = ["-- Select a relationship --"] + df["English"].tolist()
selected_relation = st.selectbox("Select relationship to edit:", options=relation_options)

if selected_relation != "-- Select a relationship --":
    idx = df[df["English"] == selected_relation].index[0]
    current = df.loc[idx]

    new_english = st.text_input("English Term", value=current["English"], key="edit_eng")
    new_hindi = st.text_input("Hindi Term", value=current["Hindi"], key="edit_hin")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Relation"):
            if new_english.strip() and new_hindi.strip():
                df.at[idx, "English"] = new_english.strip()
                df.at[idx, "Hindi"] = new_hindi.strip()
                save_data(df)
                st.success(f"✅ Updated: {new_english} - {new_hindi}")
                st.rerun()
            else:
                st.warning("⚠️ Both English and Hindi terms are required.")

    with col2:
        if st.button("Delete Relation"):
            st.session_state.undo_stack.append(df.loc[[idx]])
            df.drop(idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            save_data(df)
            st.success(f"🗑️ Deleted: {selected_relation}")
            st.rerun()

st.markdown("---")

# ⏪ Undo
if st.session_state.undo_stack:
    if st.button("Undo Last Delete"):
        restored_row = st.session_state.undo_stack.pop()
        df = pd.concat([df, restored_row], ignore_index=True)
        save_data(df)
        st.session_state.relation_df = df
        st.success(f"✅ Restored: {restored_row.iloc[0]['English']}")
        st.rerun()

st.markdown("---")

# ➕ Add Relationship
st.subheader("+ Add New Relationship")
with st.form("add_form"):
    english_term = st.text_input("English Term", key="add_eng")
    hindi_term = st.text_input("Hindi Term", key="add_hin")
    submitted = st.form_submit_button("Add")

    if submitted:
        if english_term.strip() and hindi_term.strip():
            new_row = pd.DataFrame([{"English": english_term.strip(), "Hindi": hindi_term.strip()}])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.session_state.relation_df = df
            st.success(f"✅ Added: {english_term} - {hindi_term}")
            st.rerun()
        else:
            st.warning("⚠️ Please provide both English and Hindi terms.")
