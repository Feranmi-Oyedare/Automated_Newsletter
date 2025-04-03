# Automated Research Newsletter

## Overview
This project automates the retrieval, categorization, and summarization of research articles from multiple journal repositories. The final output is a structured newsletter that highlights notable research relevant to Africa across various fields.

## Features
- **Automated Article Retrieval**: Fetches research articles from two journal repositories.
- **Topic Categorization**: Classifies articles based on their titles.
- **Newsletter Generation**: Uses OpenAI's GPT-4o to generate concise research summaries.
- **Edition Management**: Saves newsletters and sends them out monthly.

## Project Structure
```
├── datasets/                  # Stores retrieved research articles (CSV format)
│   ├── Research_Articles_Datasets.csv
│   └── ...
├── outputs/                   # Stores generated newsletters
│   ├── newsletter-latest-Edition.txt
│   └── ...
├── src/
│   ├── retrieve_articles.py   # Retrieves articles from journal repositories
│   ├── categorize_topics.py   # Categorizes articles into topics
│   ├── generate_newsletter.py # Generates the newsletter
    ├── generate_newsletter.py # Sends the newsletter
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ayonitemiferanmi/Automated_Newsletter.git
   cd automated-newsletter
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with required API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Set up your Elsevier API with the required API key:
   visit Elsevier Developer Portal: ([https://dev.elsevier.com/]). After obtaining the key, create or edit the `pybliometrics.cfg` file in the following directory:
   - **Windows**: `C:\Users\YourUsername\.config\pybliometrics\`
   - **Linux/macOS**: `~/.config/pybliometrics/`
   
   The configuration file should look like this:
   ```
   ini
   [Scopus]
   APIKey = your_scopus_api_key
   ```
5. Set up your Google App Password for sending out email:
   visit Google App Password: ([https://myaccount.google.com/apppasswords])
   ```
   set google_app_password in your .env file GOOGLE_APP_PASSWORD = "google_app_password"
   ```

## Usage
To generate the newsletter, run:
```bash
python src/generate_newsletter.py
```

To send out the newsletter as email, run:
Make sure to edit the following:
- sender email address
- receiver email address
- subject
- message
```bash
python src/send_newsletter.py
```

## Automating Newsletter Editions
The script automatically saves the latest edition each time a newsletter is generated. The latest newsletter is stored in `outputs/` with the name:
```
Newsletter-Latest-Edition.txt
```

<!-- ## Future Improvements -->
<!-- - Integration with an email service to send newsletters to subscribers. -->
<!-- - Improved topic categorization using machine learning. -->
<!-- - Web interface for user interaction. -->

## License
This project is licensed under the MIT License.

---
**Owner:** Hamoye Foundation ([www.hamoye.org]) **Maintainer:** Feranmi Ayonitemi Oyedare ([ayonitemiferanmi@gmail.com])

