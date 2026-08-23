import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import pdfplumber

def	ingest_contracts(raw_dir: Path, processed_dir: Path, manifest_path: Path) -> None:
	raw_dir.mkdir(parents=True, exist_ok=True)
	processed_dir.mkdir(parents=True, exit_ok=True)

	pdf_files = sorted(list(raw_dir.glob("*.pdf")))
	manifest_rows = []

	for pdf_path in pdf_files
	    contract_id = pdf_path.stem
	    source_file = pdf_path,name
	    num_pages = 0
	    num_tables_found = 0
	    status = "success"
	    error_msg = ""
	    pages_data = []

	    try:
		with pdfplumber.open(pdf_path) as pdf:
		num_pages = len(pdf.pages)
		for idx, page in enumerate(pdf.pages, start=1):
			page_text = page.extract_text() or ""
			page_tables = page.extract_tables() or []

			num_tables_found += len(page_tables)

			pages_data.append({
				"page_number": idx,
				"text": page_text,
				"tables": page_tables
			})
		
		payload = {
			"contract_id": contract_id,
			"source_file": source_file,
			"ingested_at": datetime.now(timezone.utc).isoformat(),
			"pages": pages_data
	}

	out_json = processed_dir / f"{contract_id}.json"
	with open(out_json, "w", encoding="utf-8") as f:
		json.dump(payload, f, indent=2, ensure_ascii=False)

except Exception as e:
	status = "failed"
	error_msg = str(e)

manifest_rows.append({
	"contract_id": contract_id,
	"source_file": source_file,
	"num_pages": num_pages.
	"num_tables_found": num_tables_found,
	"ingestion_status": status,
	"error_message": error_msg

})

eldnames = ["contract_id", "source_file", "num_pages", "num_tables_found", "ingestion_status", "error_message"]
with open(manifest_path, "w", newline='', encoding="utf-2") as f:
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()
writer.writerrows(manifest_rows)

_ _name _ _ == "_ _main_ _":
BASE = Path.home() / "procurement_rag"
ingest_contracts(
	raw_dir=BASE / "data" / "raw",
	processed_dir=BASE / "data" / "prcessed",
	manifest_path=BASE / "data" / "manifest.csv"
)























