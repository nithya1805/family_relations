import streamlit as st
import pandas as pd
import os

st.title("👨‍👩‍👧‍👦 Family Relationship Finder")

# 📁 CSV file path
CSV_FILE = r"C:\Users\13900\Downloads\llm_project\family_relationships.csv"
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# 🔄 Load data from CSV (no cache)
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)[["English", "Hindi"]]
    else:
        return pd.DataFrame(columns=["English", "Hindi"])

# 💾 Save data to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# 🔁 Reload button (optional)
if st.button("🔄 Reload from CSV file"):
    st.session_state.relation_df = load_data()
    st.success("✅ Data reloaded from file.")
    st.rerun()

# 🔃 Load into session_state only once
if "relation_df" not in st.session_state:
    st.session_state.relation_df = load_data()

# ⏪ Undo stack
if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []

df = st.session_state.relation_df

# 🔍 Search
search = st.text_input("🔍 Search relationship (English or Hindi):")
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: search.lower() in row['English'].lower() or search.lower() in row['Hindi'].lower(),
            axis=1,
        )
    ]

st.table(filtered_df)

st.markdown("---")

# ✏️ Edit Existing Relationship
st.subheader("✏️ Edit Existing Relationship")
relation_options = ["-- Select a relationship --"] + df['English'].tolist()
selected_relation = st.selectbox("Select relationship to edit:", options=relation_options)

if selected_relation != "-- Select a relationship --":
    idx = df[df['English'] == selected_relation].index[0]
    current = df.loc[idx]

    new_english = st.text_input("English Term", value=current["English"], key="edit_eng")
    new_hindi = st.text_input("Hindi Term", value=current["Hindi"], key="edit_hin")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Relation"):
            if new_english.strip() and new_hindi.strip():
                df.at[idx, 'English'] = new_english.strip()
                df.at[idx, 'Hindi'] = new_hindi.strip()
                st.session_state.relation_df = df
                save_data(df)
                st.success(f"✅ Updated: {new_english} - {new_hindi}")
                st.rerun()
            else:
                st.warning("⚠️ Both English and Hindi terms are required.")

    with col2:
        if st.button("Delete Relation"):
            st.session_state.undo_stack.append(df.loc[[idx]])
            df = df.drop(idx).reset_index(drop=True)
            st.session_state.relation_df = df
            save_data(df)
            st.success(f"🗑️ Deleted: {selected_relation}")
            st.rerun()

st.markdown("---")

# ⏪ Undo Last Delete
if st.session_state.undo_stack:
    if st.button("Undo Last Delete"):
        restored_row = st.session_state.undo_stack.pop()
        df = pd.concat([df, restored_row], ignore_index=True)
        st.session_state.relation_df = df
        save_data(df)
        st.success(f"✅ Restored: {restored_row.iloc[0]['English']}")
        st.rerun()

st.markdown("---")

# ➕ Add New Relationship
st.subheader("+ Add New Relationship")
with st.form("add_form"):
    english_term = st.text_input("English Term", key="add_eng")
    hindi_term = st.text_input("Hindi Term", key="add_hin")
    submitted = st.form_submit_button("Add")

    if submitted:
        if english_term.strip() and hindi_term.strip():
            new_row = pd.DataFrame([{"English": english_term.strip(), "Hindi": hindi_term.strip()}])
            df = pd.concat([df, new_row], ignore_index=True)
            st.session_state.relation_df = df
            save_data(df)
            st.success(f"✅ Added: {english_term} - {hindi_term}")
            st.rerun()
        else:
            st.warning("⚠️ Please provide both English and Hindi terms.")
