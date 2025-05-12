# Mood of the Queue 🎭

A Streamlit application for tracking and visualizing the emotional vibe of patient support tickets.
<img width="776" alt="Screen Shot 2025-05-10 at 11 19 40 PM" src="https://github.com/user-attachments/assets/95a8132f-1185-4a47-862f-3382096e5487" />
<img width="759" alt="Screen Shot 2025-05-10 at 11 22 04 PM" src="https://github.com/user-attachments/assets/f2534f26-6971-45ff-98bc-aae506a9a542" />


## Features ✨
- Log ticket queue moods with emoji selection (😊 😐 😠 😕 😟)
- Add optional notes for context
- Automatic timestamp recording
- Real-time visualization of daily mood trends
- Google Sheets backend for data storage

## Prerequisites 🛠️
- Python 3.7+
- Google Cloud Project with:
  - Google Sheets API enabled
  - Service account credentials

## Installation 📥
1. Clone the repository:
   ```bash
   git clone https://github.com/qiaozhou-qz/Mochi_Health_Assignment.git
   cd Mochi_Health_Assignment
2. Set Up a Virtual Environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
4. Run the Streamlit App
   ```bash
   streamlit run app.py
