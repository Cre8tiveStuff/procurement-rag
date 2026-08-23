from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

raw_dir = Path.home() / "procurement-rag" / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()

# Contract A
doc_a = SimpleDocTemplate(str(raw_dir / "contract_A_saas_license.pdf"), pagesize=letter)
doc_a.build([
    Paragraph("<b>SOFTWARE LICENSE AGREEMENT</b>", styles['Title']),
    Paragraph("<b>Section 4. Escalation</b><br/>3% annual cap.", styles['Normal']),
    Paragraph("<b>Section 12. Auto-Renewal</b><br/>45 days notice.", styles['Normal'])
])

# Contract B
doc_b = SimpleDocTemplate(str(raw_dir / "contract_B_managed_services.pdf"), pagesize=letter)
t_b = Table([['Tier', 'Fee', 'Escalation'], ['Tier 1', '$10,000', '5%/yr (capped Yr 5)']])
t_b.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black)]))
doc_b.build([
    Paragraph("<b>MANAGED SERVICES AGREEMENT</b>", styles['Title']),
    t_b,
    Paragraph("<b>Article III. Renewal</b><br/>90 days notice.", styles['Normal'])
])

# Contract C
doc_c = SimpleDocTemplate(str(raw_dir / "contract_C_equipment_lease.pdf"), pagesize=letter)
doc_c.build([
    Paragraph("<b>EQUIPMENT LEASE</b>", styles['Title']),
    Paragraph("<b>Addendum 1</b><br/>Uncapped rate increases.", styles['Normal'])
])

# Contract D
doc_d = SimpleDocTemplate(str(raw_dir / "contract_D_consulting_staffing.pdf"), pagesize=letter)
doc_d.build([
    Paragraph("<b>MASTER SERVICES AGREEMENT</b>", styles['Title']),
    Paragraph("<b>Section 1</b><br/>8% escalation.", styles['Normal'])
])

# Contract E
doc_e = SimpleDocTemplate(str(raw_dir / "contract_E_logistics_supply.pdf"), pagesize=letter)
t_e = Table([['Volume', 'Fee', 'Index'], ['1000 units', '$5.00', 'CPI-U Index']])
t_e.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black)]))
doc_e.build([
    Paragraph("<b>LOGISTICS SUPPLY</b>", styles['Title']),
    t_e,
    Paragraph("<b>Section 5</b><br/>30 days notice.", styles['Normal'])
])

print("Generated 5 sample contract PDFs in data/raw/")