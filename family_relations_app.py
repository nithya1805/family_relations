import streamlit as st
import pandas as pd
import os

CSV_FILE = "family_relationships.csv"

# Load data from CSV with caching
@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["English", "Hindi"])

# Save data to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Load into session_state
if "relation_df" not in st.session_state:
    st.session_state.relation_df = load_data()

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []

st.title("👨‍👩‍👧‍👦 Family Relationship Finder")

# 🔍 Search
search = st.text_input("🔍 Search relationship (English or Hindi):")
filtered_df = st.session_state.relation_df.copy()
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

relation_options = ["-- Select a relationship --"] + st.session_state.relation_df['English'].tolist()
selected_relation = st.selectbox("Select relationship to edit:", options=relation_options)

if selected_relation != "-- Select a relationship --":
    idx = st.session_state.relation_df[st.session_state.relation_df['English'] == selected_relation].index[0]
    current = st.session_state.relation_df.loc[idx]

    new_english = st.text_input("English Term", value=current["English"], key="edit_eng")
    new_hindi = st.text_input("Hindi Term", value=current["Hindi"], key="edit_hin")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Relation"):
            if new_english.strip() and new_hindi.strip():
                st.session_state.relation_df.at[idx, 'English'] = new_english.strip()
                st.session_state.relation_df.at[idx, 'Hindi'] = new_hindi.strip()
                save_data(st.session_state.relation_df)
                st.success(f"Updated: {new_english} - {new_hindi}")
                st.rerun()
            else:
                st.warning("Both English and Hindi terms are required.")

    with col2:
        if st.button("Delete Relation"):
            deleted_row = st.session_state.relation_df.loc[[idx]]
            st.session_state.undo_stack.append(deleted_row)
            st.session_state.relation_df = st.session_state.relation_df.drop(idx).reset_index(drop=True)
            save_data(st.session_state.relation_df)
            st.success(f"Deleted: {selected_relation}")
            st.rerun()

st.markdown("---")

# ⏪ Undo Last Delete
if st.session_state.undo_stack:
    if st.button("Undo Last Delete"):
        restored_row = st.session_state.undo_stack.pop()
        st.session_state.relation_df = pd.concat([st.session_state.relation_df, restored_row], ignore_index=True)
        save_data(st.session_state.relation_df)
        st.success(f"Restored: {restored_row.iloc[0]['English']}")
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
            st.session_state.relation_df = pd.concat([st.session_state.relation_df, new_row], ignore_index=True)
            save_data(st.session_state.relation_df)
            st.success(f"Added: {english_term} - {hindi_term}")
            st.rerun()
        else:
            st.warning("Please provide both English and Hindi terms.")
