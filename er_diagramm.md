# ER-Modell für Bananen-Supply-Chain-System

## Entity-Relationship Diagramm

```mermaid
erDiagram
    SUPPLIER ||--o{ PRODUCT : "liefert"
    PRODUCT ||--o{ ORDER_ITEM : "enthält"
    CUSTOMER ||--o{ ORDER : "bestellt"
    ORDER ||--o{ ORDER_ITEM : "enthält"
    ORDER ||--o{ DELIVERY : "wird geliefert"
    WAREHOUSE ||--o{ DELIVERY : "liefert von"
    LOGISTIKDATEN {
        int logistik_id PK
        datetime zeitstempel
        string lager
        string bananensorte
        int menge
        string lieferant
    }
    SUPPLIER {
        int supplier_id PK
        string name
        string country
    }
    PRODUCT {
        int product_id PK
        string name
        string category
        int supplier_id FK
    }
    WAREHOUSE {
        int warehouse_id PK
        string location
    }
    CUSTOMER {
        int customer_id PK
        string name
        string city
    }
    ORDER {
        int order_id PK
        int customer_id FK
        date order_date
    }
    DELIVERY {
        int delivery_id PK
        int order_id FK
        int warehouse_id FK
        date delivery_date
    }
    ORDER_ITEM {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
    }
```

## Beziehungen im Detail:

1. **Lieferant → Produkt** (1:n): Ein Lieferant kann mehrere Produkte liefern
2. **Produkt → Bestellposition** (1:n): Ein Produkt kann in vielen Bestellpositionen vorkommen
3. **Kunde → Bestellung** (1:n): Ein Kunde kann mehrere Bestellungen aufgeben
4. **Bestellung → Bestellposition** (1:n): Eine Bestellung kann mehrere Positionen haben
5. **Bestellung → Lieferung** (1:n): Eine Bestellung kann mehrere Lieferungen haben
6. **Lager → Lieferung** (1:n): Ein Lager kann mehrere Lieferungen durchführen

## Logistikdaten:
Die Tabelle `logistikdaten` ist eine separate Entität, die zeitbasierte Logistikinformationen speichert und nicht direkt mit den anderen Entitäten verknüpft ist. 