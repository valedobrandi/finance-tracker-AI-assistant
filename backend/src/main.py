from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd
import os


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
    )

def model_invoke(systemMassage: str, humanMessage: str):
     messages = [
        SystemMessage(content=systemMassage),
        HumanMessage(content=humanMessage)
        ]
     response = model.invoke(messages)
     print(response.content)
     return response.content.strip()

def tag_rows(csv_path: str):
    # Load the tagged tables
    os.makedirs("/app/src/tables", exist_ok=True)
    tagged_table = pd.read_csv("/app/src/tables/09_2025.csv")
    untagged_table = pd.read_csv(csv_path)
    examples = tagged_table.to_string(index=True)
    untagged = untagged_table.to_string(index=True)

    def to_csv_text(df, include_tag=True):
        cols = df.columns if include_tag else [c for c in df.columns if c != 'tag']
        lines = [",".join(cols)]
        for idx, row in df.iterrows():
            lines.append(",".join(str(row[c]) for c in cols))
        return "\n".join(lines)

    examples_text = to_csv_text(tagged_table)
    untagged_text = to_csv_text(untagged_table)

    systemMassage = f"Analyse this table and use as base to tag future rows:\n{examples}"
    humanMessage = f"""
        That is the untagged table:
        {untagged}

        Rules for tagging:
        - Only output lines in this exact format: index:tag
        - Output of the exact format above, one line per row without any other characters.
        - Do not include any other text, headers, extra notes or explanations.
        - tag name must match exactly as a tag in the examples table.
        - If no match found, output 'unknown' as tag.
    """
    response = model_invoke(systemMassage, humanMessage)
    print("Final response:", response)
    tag_list = response.strip().split("\n")
    for line in tag_list:
        if ":" not in line:
            continue
        index, tag = line.split(":", 1)
        try:
            index = int(index.strip())
            tag = tag.strip()
            untagged_table.at[index, 'Tag'] = tag
        except ValueError:
            print(f"Skipping invalid line: {line}")
    untagged_table.to_csv("/app/src/tables/10_2025_tagged.csv", index=False)

if __name__ == "__main__":
    # Input the CSV files and call the function
    csv = input("Enter the path to the CSV file: ")
    tag_rows(csv)