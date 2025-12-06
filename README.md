# 📘 Fynd AI Intern – Take Home Assignment

Hi! This repo contains both **Task 1** (prompt design + model evaluation) and **Task 2** (a working Streamlit app with User + Admin dashboards).  
I have tried to keep things simple, clear and easy to understand.

---

## 🚀 Live App (User + Admin)

👉 **https://fynd-ai-assignment-hobvrmv8vtfm3adxngkp8u.streamlit.app/**  
Both dashboards are in the same app — you can switch using the sidebar on the left.

---

## 📂 Project Structure

```
.
├── task1.ipynb         # Notebook for Task 1 prompts + evaluation
├── main.py             # Streamlit app (User + Admin dashboards)
├── requirements.txt    # All dependencies
├── feedback_data.csv   # Auto-created when feedback is submitted
└── README.md
```

---

# 🧠 Task 1 – Predicting Review Rating Using Prompts

In this task, I tested three different prompts to guess the star rating of a Yelp review:

1. **v1_basic** – very small and simple instruction  
2. **v2_guidelines** – added clear rules and rating guidelines  
3. **v3_few_shot** – gave a few example inputs/outputs  

### 🔍 Metrics Used
- Accuracy  
- JSON validity (whether the model returned proper JSON)

### 📊 Final Results

| Prompt Version | Accuracy | JSON Validity |
|----------------|----------|----------------|
| v1_basic       | 0.66     | 0.75           |
| v2_guidelines  | 0.47     | 0.85           |
| v3_few_shot    | 0.53     | 0.65           |

### 📝 Short Discussion

- The **basic prompt** actually worked the best for accuracy. Simple prompts don’t confuse the model.  
- The **guidelines prompt** gave the cleanest JSON, probably because the instructions were very strict.  
- The **few-shot prompt** was okay, but not very stable — sometimes worked, sometimes not.  
- Overall, more complicated prompts didn’t always give better results. Keeping things simple helped accuracy, and detailed rules helped formatting.

---

# 💬 Task 2 – AI Feedback System (Streamlit App)

For Task 2, I made a small Streamlit app with **two dashboards**.

---

## ⭐ User Dashboard

Here, users can:

- Give a rating (1–5 stars)  
- Write a review  
- Immediately get an **AI-generated polite reply**  
- The AI also creates:
  - One-line summary  
  - Suggested action items for the business  

All this gets saved into `feedback_data.csv`.

---

## 📊 Admin Dashboard

Admins can see:

- Total number of feedback submissions  
- Average user rating  
- A nice rating distribution bar chart  
- Table with all reviews + AI summary + AI actions  
- A detailed view for every single review  
- Option to download the CSV  

This helps the admin quickly understand customer sentiment and what improvements they can take.

---

# 🏗 Tech Used

- Python  
- Streamlit  
- Pandas  
- OpenRouter API  
- LLaMA 3 (8B Instruct) for generating responses  
- JSON-based prompting  

---

# 🔧 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

Add your OpenRouter key in `.streamlit/secrets.toml`:

```toml
OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
```

---

# ☁️ Deployment Info

The app is deployed on **Streamlit Cloud**.  
Secrets are stored in **Settings → Secrets** section.

---

# 📎 Report PDF

A short report explaining Task 1 and Task 2 is included separately as required.

---

# 🙌 Author

**Vivek Katariya**  
AI/ML Engineer (Intern Candidate)

If you face any issue while running the app, feel free to reach out!
