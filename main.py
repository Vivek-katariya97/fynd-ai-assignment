'''For Task 2, I made a small Streamlit app with two pages User Dashboard and Admin Dashboard.
On the user side, people can give a star rating and write their review. After they submit,
the review is sent to an AI model through OpenRouter, and it gives back three things:

>a short polite reply for the customer
>one quick summary of what the customer is saying
>a few suggesstions on what actions the buisness should take

All this data is saved in one common file (feedback_data.csv).
On the admin side, I created a simple dashboard where the admin can see:

>total number of feedbacks
>average rating
>one bar chart of rating counts
>a table with all reviews + AI summary and response
and also a detailed section for each review with the AI's recommended actions

Overall, the system is easy to use. Users give feedback,
and admins can quickly understand what customers feel and what steps they should take next.
The flow is quite smooth and everything works through the shared CSV file.'''


import streamlit as st
import pandas as pd
import json
from datetime import datetime
from openai import OpenAI
import os

# 1. OpenRouter Client

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# 2. Data Helpers

DATA_FILE = "feedback_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "timestamp", "rating", "review_text",
            "ai_response", "ai_summary", "ai_actions"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# JSON parser

import json
import re

def safe_parse_json(text: str):
    """
    Try to parse JSON from the model output.
    If it fails, try to extract the first {...} block.
    If that also fails, return a fallback structure.
    """
    # First try direct JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract a JSON object from within the text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    # Fallback if nothing works
    return {
        "ai_response": text.strip(),
        "ai_summary": "Summary not available (JSON parse failed).",
        "ai_actions": "Actions not available (JSON parse failed)."
    }


# 3. AI Function to Generate Responses

def generate_ai_outputs(rating, review_text):

    prompt = f"""
A customer left a review. Your job:

1. Write a short, polite message back to the customer.
2. Give a one-line summary of the feedback.
3. Suggest 2-3 actions the business can take.

Return ONLY JSON like this, no extra text:

{{
  "ai_response": "message to the user",
  "ai_summary": "short summary of feedback",
  "ai_actions": "bullet points of next actions"
}}

Customer Rating: {rating}
Customer Review: "{review_text}"
"""

    raw = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    text = raw.choices[0].message.content
    data = safe_parse_json(text)   # <--- use safe parser

    ai_response = data.get("ai_response", "AI response not available.")
    ai_summary  = data.get("ai_summary", "Summary not available.")
    ai_actions  = data.get("ai_actions", "Actions not available.")

    return ai_response, ai_summary, ai_actions


# 4. Streamlit UI

st.set_page_config(page_title="AI Feedback System", layout="wide")

page = st.sidebar.selectbox("Select Page", ["User Dashboard", "Admin Dashboard"])



# 5. USER DASHBOARD

if page == "User Dashboard":

    st.title("⭐ Customer Feedback")
    st.write("Share your experience with us!")

    rating = st.selectbox("How many stars would you give?", [1, 2, 3, 4, 5])
    review_text = st.text_area("Write your review here...")

    if st.button("Submit Feedback"):
        if review_text.strip() == "":
            st.warning("Please enter a review before submitting.")
        else:
            with st.spinner("AI is generating a response..."):
                ai_response, ai_summary, ai_actions = generate_ai_outputs(rating, review_text)

            # Save
            df = load_data()
            new_row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rating": rating,
                "review_text": review_text,
                "ai_response": ai_response,
                "ai_summary": ai_summary,
                "ai_actions": ai_actions
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success("Thank you! Your feedback has been submitted.")
            st.subheader("AI Response to Customer")
            st.write(ai_response)


# 6. ADMIN DASHBOARD

elif page == "Admin Dashboard":

    st.title("📊 Admin Dashboard")
    df = load_data()

    if df.empty:
        st.info("No feedback submitted yet.")
    else:
        st.subheader("Overview Stats")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Feedback", len(df))
        with col2:
            st.metric("Average Rating", round(df["rating"].mean(), 2))

        st.bar_chart(df["rating"].value_counts().sort_index())

        st.subheader("All Feedback Entries")
        st.dataframe(df)

        st.subheader("Detailed Review List")
        for index, row in df.iterrows():
            st.write(f"### ⭐ {row['rating']} - {row['timestamp']}")
            st.write(f"**User Review:** {row['review_text']}")
            st.write(f"**AI Summary:** {row['ai_summary']}")
            st.write(f"**AI Actions:** {row['ai_actions']}")
            st.markdown("---")

        st.download_button(
            label="📥 Download Feedback Data (CSV)",
            data=df.to_csv(index=False),
            file_name="feedback_data.csv",
            mime="text/csv"
            )


