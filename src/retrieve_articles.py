import os
import requests
from bs4 import BeautifulSoup
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
import pandas as pd
from datetime import datetime, timedelta
import pybliometrics
import pybliometrics.scopus
from pybliometrics.scopus.utils import create_config
import arxiv
import pandas as pd
from openai import OpenAI
from habanero import Crossref
import warnings
from dotenv import load_dotenv
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Set up OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get today's date and the date one month ago
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# Set up Scopus Elsevier API
api_keys = [os.getenv('SCOPUS_API_KEY')] 

# Create configuration file
create_config(keys=api_keys)
print("Configuration file created successfully.")

def retrieve_scopus_data():
    pybliometrics.scopus.init()
    # Define the query
    query = f'''(TITLE-ABS-KEY(Africa OR Nigeria OR Kenya OR Ghana OR South Africa OR Liberia OR Egypt OR Lagos OR Abuja OR Morocco OR Rwanda OR Senegal OR "Sub-Saharan Africa")) 
            AND (DOCTYPE(AR)) 
            AND (SRCTYPE(j)) 
            AND (ORIG-LOAD-DATE > {start_date} AND ORIG-LOAD-DATE < {end_date})'''

    # Perform Scopus search
    x = ScopusSearch(query=query, view="STANDARD", cursor=None, verbose=True)
    
    # Extract results
    scopus_data = []
    for result in x.results:
        scopus_data.append({
            "Title": result.title,
            "Author": result.creator,
            "Publication_Year": result.coverDate,
            "Link": f"http://dx.doi.org/{result.doi}" if result.doi else "No DOI available"
        })
    
    scopus_df = pd.DataFrame(scopus_data)

    # Ensure only results within the date range
    scopus_df = scopus_df[
        (scopus_df["Publication_Year"] >= start_date) & 
        (scopus_df["Publication_Year"] <= end_date)
    ].reset_index(drop=True)

    # Fetch abstracts using Crossref from Habanero
    cr = Crossref()
    abstracts = []
    
    for link in scopus_df["Link"]:
        if "No DOI available" in link:
            abstracts.append("No abstract available")
            continue
        
        doi = link.split("doi.org/")[-1]
        try:
            paper = cr.works(ids=doi)
            abstract_raw = paper["message"].get("abstract", "No abstract available")
            soup = BeautifulSoup(abstract_raw, "html.parser")
            abstracts.append(soup.get_text())
        except Exception as e:
            abstracts.append("No abstract available")  # Handle errors gracefully

    scopus_df["Abstract"] = abstracts

    # Remove rows with no abstracts
    scopus_df = scopus_df[scopus_df["Abstract"] != "No abstract available"]

    print("<====== Extracted Scopus[Elsevier] Articles ======>")
    # return the dataframe
    return scopus_df

def retrieve_arxiv_data(max_results=30):
    
    # Define the list of keywords to search for
    keywords = ["Africa", "Nigeria", "Kenya", "Ghana", "South Africa", "Liberia", "Egypt", "Lagos", "Abuja", "Morocco", "Rwanda", "Senegal", "Sub-Saharan Africa"]

    # Construct the OR-based search query
    query = " OR ".join(keywords)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    new_data = []
    for result in search.results():
        new_data.append({
          "Title": result.title,
          "Author": result.authors,
          "Publication_Year": str(result.published.date()),
          "Link": result.pdf_url,
          "Abstract": result.summary
        })

    arxiv_df = pd.DataFrame(new_data)

    # Filter out the Publication Date
    arxiv_df["Publication_Year"].astype(str)
    arxiv_df = arxiv_df[(arxiv_df["Publication_Year"] >= str(start_date)) & (arxiv_df["Publication_Year"] <= str(end_date))]

    # Reset the index of the Dataframe
    arxiv_df = arxiv_df.reset_index(drop=True)

    print("<====== Extracted arXiv Articles ======>")
    # Return the dataframe
    return arxiv_df


def merge_dataframes():
    scopus_df = retrieve_scopus_data()
    arxiv_df = retrieve_arxiv_data()  
    df = pd.concat([scopus_df, arxiv_df], axis=0)

    df.reset_index(drop=True)

    print("<====== Successfully merged the datasets ======>")
    return df


if __name__ == "__main__":
    merge_dataframes()
    