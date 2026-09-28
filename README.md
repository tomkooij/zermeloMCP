# Zermelo MCP Server

Een krachtige **Model Context Protocol (MCP) server** geschreven in Python om data uit de **Zermelo API** (roostersoftware voor het onderwijs) te lezen en schrijven.

Met deze MCP server kunnen AI-assistenten (zoals Claude Desktop, Gemini, Cursor, en Antigravity) rechtstreeks communiceren met Zermelo om roosters op te vragen, afspraken/lessen in te plannen of aan te passen, mededelingen te beheren en schoolgegevens uit te lezen.

---

## ⚡ Functionaliteiten

### 📖 Lezen (Read Operations)
* **`get_appointments`**: Roosterafspraken ophalen voor een leerling, docent (`~me` of code), groep of lokaal binnen een datum/tijdvenster.
* **`get_users`**: Gebruikers (leerlingen, docenten, medewerkers) zoeken en bekijken.
* **`get_groups`**: Klassen en lesgroepen opvragen.
* **`get_locations`**: Lokalen en ruimtes opvragen.
* **`get_subjects`**: Vakken opvragen.
* **`get_announcements`**: Schoolmededelingen inzien.
* **`get_participations`**: Afspraakdeelnames bekijken.
* **`get_school_in_school_years`**: Schooljaren en koppelings-IDs ophalen.
* **`get_partner_me`**: Partner-rechten en toegangsrechten inzien (`/partners/~me`).

### ✍️ Schrijven (Write Operations)
* **`create_appointment`**: Nieuwe afspraak/les aanmaken in het rooster.
* **`update_appointment`**: Bestaande afspraak of roosterwijziging aanpassen.
* **`delete_appointment`**: Afspraak annuleren/verwijderen uit het rooster.
* **`create_announcement`**: Nieuwe mededeling plaatsen.
* **`update_announcement`**: Mededeling bewerken.
* **`delete_announcement`**: Mededeling verwijderen.
* **`add_participation`**: Deelnemer (leerling/docent/groep) toevoegen aan een afspraak.
* **`remove_participation`**: Deelnemer verwijderen uit een afspraak.
* **`exchange_auth_code`**: Eenmalige 12-cijferige Koppelcode / Auth Code omwisselen voor een API token.

---

## 🚀 Installatie & Snelle Start

### 1. Vereisten
* Python 3.10 of hoger
* `uv` of `pip`

### 2. Virtuele omgeving aanmaken en afhankelijkheden installeren
```bash
# Met uv (aanbevolen)
uv venv
uv pip install -e .

# Of met standaard pip
python -m venv .venv
.venv\Scripts\activate   # Op Windows
pip install -e .
```

---

## ⚙️ Configuraties (Omgevingsvariabelen)

De Zermelo MCP server kan geconfigureerd worden via de volgende omgevingsvariabelen:

| Variabele | Omschrijving | Voorbeeld |
| :--- | :--- | :--- |
| `ZERMELO_SCHOOL` | Naam van de school (of subdomein / URL) | `mijnschool` of `mijnschool.zportal.nl` |
| `ZERMELO_TOKEN` | OAuth2 / API Access Token van Zermelo | `abc123def456...` |
| `ZERMELO_API_VERSION` | API Versie (standaard: `v3`) | `v3` |

> 💡 **Flexibele parameters:** U kunt de `school` en `token` ook per tool-call meegeven als optionele argumenten.

---

## 💻 Integratie met MCP Clients

### Claude Desktop Configuration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "zermelo": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/Tom/github/zermeloMCP",
        "run",
        "zermelo-mcp"
      ],
      "env": {
        "ZERMELO_SCHOOL": "jouwschool",
        "ZERMELO_TOKEN": "jouw_api_token"
      }
    }
  }
}
```

### Direct via de CLI starten
```bash
# Stdio transport (standaard voor MCP clients)
zermelo-mcp

# SSE transport (webserver modus)
zermelo-mcp --transport sse --port 8000
```

---

## 🛠️ Voorbeelden van gebruik via MCP

* **Rooster opvragen:**
  > *"Laat mijn rooster van vandaag zien voor school `mijnschool`."*
* **Lesuitval / Roosterwijziging aanmaken:**
  > *"Maak een afspraak aan voor vak `wisa` met docent `abc` in lokaal `101` morgen om 09:00."*
* **Auth Code omwisselen:**
  > *"Wissel de Zermelo koppelcode `123 456 789 012` om voor een API token."*

---

## 📄 Licentie
MIT License
