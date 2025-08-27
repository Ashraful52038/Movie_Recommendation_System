# Movie_Recommendation_System
This is a content-based movie recommendation system built with Python, Streamlit, and Machine Learning. It suggests movies similar to the one you select, along with their posters fetched from TMDB API.
Recommendation Algorithm: Content-Based Filtering with Cosine Similarity on movie metadata.

🚀 Features
Search and select any movie from the list
Get top 5 similar movies instantly
Movie posters are fetched dynamically from TMDB API
Simple web app interface powered by Streamlit

🛠️ Installation
Clone the repository:
git clone https://github.com/Ashraful52038/Movie_Recommendation_System.git
cd Movie_Recommendation_System

Install dependencies:
pip install -r requirements.txt

▶️ Run the App Locally
streamlit run app.py
Then open your browser at http://localhost:8501/

🌍 Deployment (Render + Hugging Face)

Since .pkl files can be large, we hosted them on Hugging Face Datasets and downloaded them dynamically inside the Streamlit app.
Steps I followed:
1.Created a Hugging Face dataset repo and uploaded:
movie_dict.pkl
similarity.pkl

2.Used the requests library in app.py to fetch and save them locally at runtime:
def download_from_hf(url, destination):
    if os.path.exists(destination):
        return  
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
3.Deployed to Render:
  Added a requirements.txt
  Configured Start Command as:
    streamlit run app.py --server.port $PORT --server.address 0.0.0.0
4.Render automatically installs dependencies and runs the app online.

⚡ My Struggles During Deployment
This project wasn’t smooth from the start — here’s the path I went through:
❌ GitHub file size limit:
GitHub does not allow committing files larger than 100 MB.
Since my movies_dict.pkl and similarity.pkl files were larger than that, I couldn’t push them to GitHub.
That’s where my suffering started.
❌ Heroku attempt failed:
I tried to deploy on Heroku, but since it now requires credit card verification, I couldn’t continue because of financial issues.
❌ Render attempt (pickle error):
I then switched to Render, but it failed because the .pkl files were too big.
When I tried uploading them, Render gave me:

🔑 API Key Setup
This project uses the TMDB API for fetching posters.
API_KEY = "267fdd6ab0dfe7bee4813dd75e6f979b"

📸 Demo
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/21d41dd3-210a-4725-a53c-6678cc650897" />




🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

