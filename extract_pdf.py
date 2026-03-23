import pdfplumber
import pandas as pd

# Change this to your pdf path
PDF_PATH = "data/unlearn_2018.pdf"
YEAR = 2018

all_tables = []

with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table)
            all_tables.append(df)
        print(f"Page {i+1}: {len(tables)} tables found")

# Save raw extraction to inspect
combined = pd.concat(all_tables, ignore_index=True)
combined.to_csv(f"data/raw_pdf_{YEAR}.csv", index=False)
print(f"Done! {len(all_tables)} tables extracted")
