from openai import OpenAI
from dotenv import load_dotenv
import os
from retrieve_articles import merge_dataframes

# Load environment variables
load_dotenv()

# Ensure 'data' directory exists
os.makedirs("data", exist_ok=True)

# Initializing OpenAI's client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def categorize_topics():
    df = merge_dataframes()

    topic_category = []
    for title in df["Title"]:
        # Query OpenAI API for topic categorization
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant. Given a research paper title, classify it into a relevant academic category. Your response should only contain the category name."
                },
                {
                    "role": "user",
                    "content": f"Categorize the research paper titled: '{title}'. Only return the topic category."
                }
            ],
            temperature=0  # Ensures consistency in responses
        )

        # Extract and print topic categorization
        topic_categorization = completion.choices[0].message.content.strip()
        topic_category.append(topic_categorization)

    # Merge topic categories to the dataframe
    df["Topic_Category"] = topic_category

    # Reset the index of the dataframe
    df.reset_index(drop=True, inplace=True)

    print("<====== Successfully Categorized the Research Article Topics ======>")
    # Export the merged dataset in form of csv file to the data folder
    # os.chdir("../") # Change directory to the parent folder
    df.to_csv(f"data/Research_Articles_Datasets.csv")
    print("<====== Dataset Successfully Saved to Data Folder ======>")
    # Return the dataframe with topic categories
    return df

if __name__ == "__main__":
    categorize_topics()