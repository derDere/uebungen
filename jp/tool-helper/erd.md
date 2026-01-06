## Entitäten und Attribute

### ERD (Konzeptionelles Modell)

```mermaid
erDiagram

    TOOL {
        string name
        string status
    }

    CHECK_LIST {
        string name
        string status
    }

    CHECK_LIST_TEMPLATE {
        string name
        string status
    }

    CHECK_LIST_POINT {
        string name
        string status
        bool is_checked
    }

    CHECK_LIST_POINT_TEMPLATE {
        string name
        string datatype
    }

    TOOL ||--o{ CHECK_LIST : besitzt
    CHECK_LIST_TEMPLATE ||--o{ CHECK_LIST : basiert-auf
    CHECK_LIST }o--o{ CHECK_LIST_POINT : enthaelt
    CHECK_LIST_TEMPLATE }o--o{ CHECK_LIST_POINT_TEMPLATE : definiert
    CHECK_LIST_POINT_TEMPLATE ||--o{ CHECK_LIST_POINT : instanziiert

```

### TOOL

* **id** (PK, int)
* name (str)
* status (enum)

---

### CHECK_LIST

* **id** (PK, int)
* name (str)
  _toggle--??
  Wait.

Let's read diagram carefully mentally.

Entities:

TOOL
id PK int
name str
status enum
(Row 3 placeholder ignore)

CHECK_LIST
id PK int
name str
status enum

CHECK_LIST_TEMPLATE
id PK int
name str
status enum

CHECK_LIST_POINT
id PK int
name str
status enum
is_checked bool

CHECK_LIST_POINT_TEMPLATE
id PK int
name str
datatype ? (probably enum or str, shown as "datatype?")

Junction tables:

CHECK_LIST_CHECK_LIST_POINT
(name shown as "CHECK LIST CHECK LIST POINT")

* check_list_id (FK, int)
* check_list_point_id (FK, int)

CHECK_LIST_TEMPLATE_CHECK_LIST_POINT
(name shown as "CHECK LIST TEMPLATE CHECK LIST POINT")

* check_list_temp_id (FK, int)
* check_list_point_temp_id (FK, int)

---

## Beziehungen (Kardinalitäten)

1. TOOL ↔ CHECK_LIST

* TOOL (1) —— (0..N) CHECK_LIST
  → Ein Tool hat 0 bis N Checklisten
  → Eine Checkliste gehört genau zu einem Tool

2. CHECK_LIST ↔ CHECK_LIST_TEMPLATE

* CHECK_LIST_TEMPLATE (1) —— (0..N) CHECK_LIST
  → Eine Checklisten-Vorlage kann für 0 bis N Checklisten verwendet werden
  → Eine Checkliste basiert auf genau einer Vorlage

3. CHECK_LIST ↔ CHECK_LIST_POINT (Many-to-Many)

* Realisiert über **CHECK_LIST_CHECK_LIST_POINT**
* CHECK_LIST (1) —— (0..N) CHECK_LIST_CHECK_LIST_POINT
* CHECK_LIST_POINT (1) —— (0..N) CHECK_LIST_CHECK_LIST_POINT

→ Eine Checkliste enthält 0 bis N Checklisten-Punkte
→ Ein Checklisten-Punkt kann in 0 bis N Checklisten vorkommen

4. CHECK_LIST_TEMPLATE ↔ CHECK_LIST_POINT_TEMPLATE (Many-to-Many)

* Realisiert über **CHECK_LIST_TEMPLATE_CHECK_LIST_POINT**
* CHECK_LIST_TEMPLATE (1) —— (0..N) CHECK_LIST_TEMPLATE_CHECK_LIST_POINT
* CHECK_LIST_POINT_TEMPLATE (1) —— (0..N) CHECK_LIST_TEMPLATE_CHECK_LIST_POINT

→ Eine Checklisten-Vorlage enthält 0 bis N Punkt-Vorlagen
→ Eine Punkt-Vorlage kann in 0 bis N Checklisten-Vorlagen vorkommen

5. CHECK_LIST_POINT_TEMPLATE ↔ CHECK_LIST_POINT

* CHECK_LIST_POINT_TEMPLATE (1) —— (0..N) CHECK_LIST_POINT
  → Aus einer Punkt-Vorlage entstehen 0 bis N konkrete Checklisten-Punkte
  → Jeder Checklisten-Punkt basiert auf genau einer Punkt-Vorlage

### Relationales Datenbank Model (Physisches Modell)

```mermaid
erDiagram

    TOOL {
        int id PK
        varchar name
        enum status
        datetime created_at
        datetime updated_at
    }

    CHECK_LIST {
        int id PK
        varchar name
        enum status
        int tool_id FK
        int check_list_template_id FK
        datetime created_at
        datetime updated_at
    }

    CHECK_LIST_TEMPLATE {
        int id PK
        varchar name
        enum status
        datetime created_at
        datetime updated_at
    }

    CHECK_LIST_POINT {
        int id PK
        varchar name
        enum status
        boolean is_checked
        int check_list_point_template_id FK
        datetime created_at
        datetime updated_at
    }

    CHECK_LIST_POINT_TEMPLATE {
        int id PK
        varchar name
        varchar datatype
        datetime created_at
        datetime updated_at
    }

    CHECK_LIST_CHECK_LIST_POINT {
        int check_list_id PK
        int check_list_point_id PK
        datetime created_at
    }

    CHECK_LIST_TEMPLATE_POINT_TEMPLATE {
        int check_list_template_id PK
        int check_list_point_template_id PK
        int sort_order
        datetime created_at
    }

    TOOL ||--o{ CHECK_LIST : tool_id
    CHECK_LIST_TEMPLATE ||--o{ CHECK_LIST : template_id
    CHECK_LIST_POINT_TEMPLATE ||--o{ CHECK_LIST_POINT : template_id
    CHECK_LIST ||--o{ CHECK_LIST_CHECK_LIST_POINT : check_list_id
    CHECK_LIST_POINT ||--o{ CHECK_LIST_CHECK_LIST_POINT : point_id
    CHECK_LIST_TEMPLATE ||--o{ CHECK_LIST_TEMPLATE_POINT_TEMPLATE : template_id
    CHECK_LIST_POINT_TEMPLATE ||--o{ CHECK_LIST_TEMPLATE_POINT_TEMPLATE : point_template_id

```