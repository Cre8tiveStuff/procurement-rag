import os
import glob
import pandas as pd
import pypdf

def ingest_pdfs():
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(raw_dir, "*.pdf"))
    manifest_data = []
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        reader = pypdf.PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
            
        text_filename = filename.replace(".pdf", ".txt")
        text_path = os.path.join(processed_dir, text_filename)
        
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        manifest_data.append({
            "filename": filename,
            "raw_path": pdf_path,
            "processed_path": text_path,
            "page_count": num_pages
        })
        
    df = pd.DataFrame(manifest_data)
    df.to_csv("data/manifest.csv", index=False)
    print(f"Ingested {len(pdf_files)} PDFs. Manifest created at data/manifest.csv")

if __name__ == "__main__":
    ingest_pdfs()