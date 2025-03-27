from openai import OpenAI
from dotenv import load_dotenv
import os
from categorize_topics import categorize_topics

# Load environment variables
load_dotenv()

# Initializing OpenAI's client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def generate_newsletter():
    # Load the dataframe
    df = categorize_topics()

    # Format newsletter content
    newsletter_content = "Research Newsletter\n\n"
    newsletter_content += "Welcome to this edition of our research newsletter, where we summarize notable research articles relating to Africa across various fields.\n\n"

    print("<====== Generating the Newsletter ======>")

    count = 1
    for topic in df["Topic_Category"].unique():
        categorized_df = df[df["Topic_Category"] == topic]

        # Extract information as lists
        titles = categorized_df["Title"].tolist()
        authors = categorized_df["Author"].tolist()
        abstracts = categorized_df["Abstract"].tolist()
        links = categorized_df["Link"].tolist()

        # Format input for OpenAI
        research_papers = "\n".join([f"- **{t}** by {a} ([Link]({l}))" for t, a, l in zip(titles, authors, links)])
        abstracts_text = "\n".join([f"{i+1}. {ab}" for i, ab in enumerate(abstracts)])

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are an academic assistant summarizing research papers for a newsletter. 
                        Given a set of research titles, authors, abstracts, and links, 
                        create a concise yet comprehensive summary for each topic category.
                        
                        - The summary should be **two paragraphs long**.
                        - Incorporate key insights from all research papers under the category.
                        - Ensure clarity and engagement while maintaining academic rigor.
                        - Provide a smooth transition between key ideas.
                        - Use simple, professional language.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                        **Topic Category:** {topic}

                        **Research Papers:**
                        {research_papers}

                        **Abstracts:**
                        {abstracts_text}

                        Generate a well-structured summary that highlights the key insights from these research papers in two paragraphs.
                    """
                }
            ],
            temperature=0  # Ensures consistency
        )

        # Extract and append to the newsletter
        section_summary = completion.choices[0].message.content.strip()
        newsletter_content += f"{count}) {topic}\n\n{section_summary}\n\n{'==' * 68}\n\n"
        count += 1

    # Print or save the newsletter
    with open(f"outputs/Newsletter-Latest-Edition.txt", "w", encoding="utf-8") as f:
        f.write(newsletter_content)
        print(f"Newsletter content saved as Newsletter-Latest-Edition.txt")

if __name__ == "__main__":
    generate_newsletter()