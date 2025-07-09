from sqlalchemy import create_engine, text
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def get_order_data(order_id):
    """Holt detaillierte Bestelldaten aus der Datenbank"""
    query = """
        SELECT 
            o.id as order_id,
            o.order_date,
            c.name as customer_name,
            c.city as customer_city,
            p.name as product_name,
            p.category,
            oi.quantity,
            s.name as supplier_name,
            s.country as supplier_country,
            w.location as warehouse_location
        FROM "order" o
        JOIN customer c ON o.customer_id = c.id
        JOIN order_item oi ON o.id = oi.order_id
        JOIN product p ON oi.product_id = p.id
        JOIN supplier s ON p.supplier_id = s.id
        LEFT JOIN delivery d ON o.id = d.order_id
        LEFT JOIN warehouse w ON d.warehouse_id = w.id
        WHERE o.id = :order_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"order_id": order_id})
        return result.fetchall()

def create_header_footer(canvas, doc):
    """Erstellt Header und Footer für jede Seite"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(50, A4[1] - 50, "BANANA SUPPLY CHAIN")
    canvas.setFont('Helvetica', 10)
    canvas.drawString(50, A4[1] - 70, "Bestellschein")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.drawString(50, 30, f"Generiert am: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    canvas.drawRightString(A4[0] - 50, 30, f"Seite {doc.page}")
    
    canvas.restoreState()

def create_order_pdf_advanced(order_id, output_path="bestellschein_advanced.pdf"):
    """Erstellt einen erweiterten PDF-Bestellschein mit professionellem Design"""
    
    # Bestelldaten abrufen
    order_data = get_order_data(order_id)
    
    if not order_data:
        print(f"Keine Daten für Bestellung {order_id} gefunden!")
        return
    
    # PDF-Dokument erstellen
    doc = SimpleDocTemplate(output_path, pagesize=A4, 
                          rightMargin=2*cm, leftMargin=2*cm, 
                          topMargin=3*cm, bottomMargin=2*cm)
    story = []
    
    # Styles definieren
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.darkgreen
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=5
    )
    
    # Header
    story.append(Paragraph("BESTELLSCHEIN", title_style))
    story.append(Spacer(1, 20))
    
    # Bestellinformationen
    first_row = order_data[0]
    
    # Linke Spalte - Bestelldetails
    order_info_left = [
        ["Bestellnummer:", str(first_row.order_id)],
        ["Bestelldatum:", first_row.order_date.strftime("%d.%m.%Y")],
        ["Kunde:", first_row.customer_name],
        ["Stadt:", first_row.customer_city]
    ]
    
    # Rechte Spalte - Lieferdetails
    warehouse_info = first_row.warehouse_location if first_row.warehouse_location else "Nicht zugewiesen"
    order_info_right = [
        ["Lieferant:", first_row.supplier_name],
        ["Land:", first_row.supplier_country],
        ["Lager:", warehouse_info],
        ["Status:", "Bestellt"]
    ]
    
    # Tabelle für Bestellinformationen
    order_info_data = []
    for i in range(len(order_info_left)):
        order_info_data.append([
            order_info_left[i][0], order_info_left[i][1],
            order_info_right[i][0], order_info_right[i][1]
        ])
    
    order_table = Table(order_info_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    order_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(order_table)
    story.append(Spacer(1, 30))
    
    # Bestellpositionen
    story.append(Paragraph("Bestellpositionen", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Tabellenkopf
    table_data = [["Pos.", "Produkt", "Kategorie", "Menge", "Einheit"]]
    
    # Bestellpositionen hinzufügen
    for i, row in enumerate(order_data, 1):
        table_data.append([
            str(i),
            row.product_name,
            row.category,
            str(row.quantity),
            "Stück"
        ])
    
    # Tabelle erstellen
    items_table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Produktname linksbündig
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    story.append(items_table)
    
    # Zusammenfassung
    story.append(Spacer(1, 30))
    
    # Gesamtmenge berechnen
    total_quantity = sum(row.quantity for row in order_data)
    unique_products = len(set(row.product_name for row in order_data))
    
    summary_data = [
        ["Anzahl Produkte:", str(unique_products)],
        ["Gesamtmenge:", f"{total_quantity} Stück"],
        ["Erstellt am:", datetime.now().strftime("%d.%m.%Y %H:%M")]
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(summary_table)
    
    # Hinweise
    story.append(Spacer(1, 20))
    story.append(Paragraph("Hinweise:", info_style))
    story.append(Paragraph("• Dieser Bestellschein wurde automatisch generiert", info_style))
    story.append(Paragraph("• Bei Fragen wenden Sie sich an den Support", info_style))
    story.append(Paragraph("• Bestellungen werden innerhalb von 24h bearbeitet", info_style))
    
    # PDF generieren mit Header/Footer
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    print(f"Erweiterter Bestellschein wurde erstellt: {output_path}")

def generate_all_order_pdfs():
    """Generiert PDFs für alle verfügbaren Bestellungen"""
    query = """
        SELECT DISTINCT o.id, o.order_date, c.name as customer_name
        FROM "order" o
        JOIN customer c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
        LIMIT 5
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        orders = result.fetchall()
    
    if not orders:
        print("Keine Bestellungen in der Datenbank gefunden!")
        return
    
    # PDF-Ordner erstellen
    pdf_folder = "bestellscheine"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    print(f"Generiere PDFs für {len(orders)} Bestellungen...")
    
    for order in orders:
        filename = f"{pdf_folder}/bestellschein_{order.id}_{order.order_date.strftime('%Y%m%d')}.pdf"
        try:
            create_order_pdf_advanced(order.id, filename)
            print(f"✓ Bestellung {order.id} ({order.customer_name})")
        except Exception as e:
            print(f"✗ Fehler bei Bestellung {order.id}: {e}")
    
    print(f"\nAlle PDFs wurden im Ordner '{pdf_folder}' gespeichert!")

if __name__ == "__main__":
    print("=== PDF Bestellschein Generator ===")
    print("1. Einzelnen Bestellschein generieren")
    print("2. Alle Bestellscheine generieren")
    
    choice = input("Wählen Sie eine Option (1 oder 2): ").strip()
    
    if choice == "1":
        # Verfügbare Bestellungen anzeigen
        query = """
            SELECT o.id, o.order_date, c.name as customer_name
            FROM "order" o
            JOIN customer c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
            LIMIT 10
        """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            orders = result.fetchall()
        
        if orders:
            print("\nVerfügbare Bestellungen:")
            print("ID | Datum | Kunde")
            print("-" * 50)
            for order in orders:
                print(f"{order.id} | {order.order_date.strftime('%d.%m.%Y')} | {order.customer_name}")
            
            try:
                order_id = int(input("\nGeben Sie die Bestell-ID ein: "))
                create_order_pdf_advanced(order_id, f"bestellschein_{order_id}.pdf")
            except ValueError:
                print("Ungültige Eingabe!")
        else:
            print("Keine Bestellungen gefunden!")
    
    elif choice == "2":
        generate_all_order_pdfs()
    
    else:
        print("Ungültige Auswahl!") 