# **WorkoutPlan**

An application that integrates with the **Strava API** to fetch and analyze my fitness activities, generate personalized fitness advice and motivation using a **LLM (Large Language Model)**, and deliver insights via **email notifications**.

---

## **Features**

- **Strava Integration:**  
   - Fetch recent activities such as runs, rides, and hikes.  
   - Process fitness data and calculate metrics that are personalized to my specific goals. 
   - Automatic token management and refresh.

- **Personalized Fitness Insights:**  
   - LLM: **Mistral-7B-Instruct-v0.3** via Hugging Face Inference API to generate actionable fitness advice.  
   - Stream real-time fitness recommendations.

- **Webhook Support:**  
   - Automatically process new activities via **Strava Webhooks**.  
   - Ensure each activity is processed only once using **persistent tracking (SQLite)**.

- **Email Notifications:**  
   - Send automated fitness insights and workout summaries via email.

- **Lightweight and Deployable:**   
   - Currently deployed on **Heroku**.

---

## **Tech Stack**

- **Backend Framework:** FastAPI, Python 
- **Database:** SQLite  
- **LLM Model:** Mistral-7B-Instruct-v0.3 (via Hugging Face Inference API)  
- **Email Notifications:** SMTP  
- **Webhook Handling:** FastAPI Routes  
---