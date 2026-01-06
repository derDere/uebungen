# Fragen:

### 1. **Projektstruktur & Setup**

* Soll das Projekt ein **SvelteKit** Projekt sein oder ein normales Svelte SPA?
* Soll SQLite **lokal im Browser** (z. B. via `sql.js`) oder serverseitig (z. B. Node + `better-sqlite3`) laufen?
* Soll es ein **Backend** geben oder alles nur clientseitig?
* Willst du **TypeScript** nutzen oder plain JavaScript?

antworten: SPA, backend mit fastapi (python) und typescript

---

### 2. **Datenmodell**

* Soll die Datenbank **alle Tabellen wie im ERD** direkt abbilden oder willst du einige Tabellen zusammenfassen/simplifizieren?
* Welche Datentypen sollen konkret für `status` Enum verwendet werden? (z. B. `active/inactive`, `draft/published`, …)
* Soll `datatype` in `CHECK_LIST_POINT_TEMPLATE` nur `string` sein oder bestimmte Typen unterstützen (`text`, `number`, `boolean`, …)?
* Sollen `created_at` und `updated_at` automatisch gepflegt werden oder manuell gesetzt werden?

antworten: ja wie im erd, aber egal hauptsache funktioniert und mit SQLite

---

### 3. **Beziehungen & Funktionalität**

* Soll die Many-to-Many Beziehung zwischen Checklisten und Punkten **über eine echte Junction Table** oder nur per Array/ID-Liste umgesetzt werden?
* Soll ein Checklisten-Punkt **immer nur von einer Vorlage abstammen** oder auch unabhängig erstellt werden können?
* Soll die **Sortierung** der Punkte in einer Checkliste wichtig sein?

antworten: verknüpfungstabelle, auch unabhängig erzeugen, alphabetich

---

### 4. **UI / UX**

* Soll das UI **nur CRUD für alle Entities** sein oder sollen auch Checklisten **abgehakt werden** können?
* Soll es **Templates auswählen / instanziieren** geben oder eher manuell?
* Soll die Anzeige der Checklisten **nested** sein (Tool → Checkliste → Punkte)?
* Soll die Statusänderung **live** in der DB gespeichert werden oder nur beim Speichern?

antworten: auch abhacken, templates bearbeiten erstellen und nutzen, ja live

---

### 5. **Extras / Features**

* Soll es **Such- und Filterfunktion** nach Tools, Checklisten oder Punkten geben?
* Soll es eine **Export-/Import-Funktion** geben (JSON/CSV)?
* Willst du **Unit-Tests** oder nur ein simples Übungsprojekt?

antworten: ja such und filter ist gut, ja export als csv md yaml und json, nein keine unit tests