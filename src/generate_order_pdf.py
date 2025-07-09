from sqlalchemy import create_engine, text
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB = "supplychain"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def get_order_data(order_id):
    """Holt Bestelldaten aus der Datenbank"""
    query = """
        SELECT 
            o.id as order_id,
            o.order_date,
            c.name as customer_name,
            c.city as customer_city,
            p.name as product_name,
            p.category,
            oi.quantity,
            s.name as supplier_name
        FROM "order" o
        JOIN customer c ON o.customer_id = c.id
        JOIN order_item oi ON o.id = oi.order_id
        JOIN product p ON oi.product_id = p.id
        JOIN supplier s ON p.supplier_id = s.id
        WHERE o.id = :order_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"order_id": order_id})
        return result.fetchall()

def create_order_pdf(order_id, output_path="bestellschein.pdf"):
    """Erstellt einen PDF-Bestellschein"""
    
    # Bestelldaten abrufen
    order_data = get_order_data(order_id)
    
    if not order_data:
        print(f"Keine Daten für Bestellung {order_id} gefunden!")
        return
    
    # PDF-Dokument erstellen
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    
    # Styles definieren
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Zentriert
    )
    
    # Header
    story.append(Paragraph("BESTELLSCHEIN", title_style))
    story.append(Spacer(1, 20))
    
    # Bestellinformationen
    first_row = order_data[0]
    order_info = [
        ["Bestellnummer:", str(first_row.order_id)],
        ["Bestelldatum:", first_row.order_date.strftime("%d.%m.%Y")],
        ["Kunde:", f"{first_row.customer_name}, {first_row.customer_city}"],
        ["Lieferant:", first_row.supplier_name]
    ]
    
    order_table = Table(order_info, colWidths=[2*inch, 4*inch])
    order_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(order_table)
    story.append(Spacer(1, 20))
    
    # Bestellpositionen
    story.append(Paragraph("Bestellpositionen:", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    # Tabellenkopf
    table_data = [["Produkt", "Kategorie", "Menge"]]
    
    # Bestellpositionen hinzufügen
    for row in order_data:
        table_data.append([
            row.product_name,
            row.category,
            str(row.quantity)
        ])
    
    # Tabelle erstellen
    items_table = Table(table_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(items_table)
    
    # Gesamtmenge berechnen
    total_quantity = sum(row.quantity for row in order_data)
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Gesamtmenge: {total_quantity} Einheiten", styles['Normal']))
    
    # PDF generieren
    doc.build(story)
    print(f"Bestellschein wurde erstellt: {output_path}")

def list_available_orders():
    """Zeigt alle verfügbaren Bestellungen an"""
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
    
    print("Verfügbare Bestellungen:")
    print("ID | Datum | Kunde")
    print("-" * 50)
    for order in orders:
        print(f"{order.id} | {order.order_date.strftime('%d.%m.%Y')} | {order.customer_name}")
    
    return [order.id for order in orders]

if __name__ == "__main__":
    # Verfügbare Bestellungen anzeigen
    available_orders = list_available_orders()
    
    if available_orders:
        # Erste Bestellung als Beispiel generieren
        first_order = available_orders[0]
        create_order_pdf(first_order, f"bestellschein_{first_order}.pdf")
        
        print(f"\nPDF für Bestellung {first_order} wurde erstellt!")
        print("Sie können auch andere Bestellungen generieren, indem Sie die order_id ändern.")
    else:
        print("Keine Bestellungen in der Datenbank gefunden!") 