<h1 align="center">TripMind AI</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-in%20progress-f59e0b.svg" alt="Status">
  <a href="https://github.com/Vishuu_Patil_001/TripMind-AI/issues"><img src="https://img.shields.io/github/issues/Vishuu_Patil_001/TripMind-AI.svg" alt="GitHub Issues"></a>
  <a href="https://github.com/Vishuu_Patil_001/TripMind-AI/pulls"><img src="https://img.shields.io/github/issues-pr/Vishuu_Patil_001/TripMind-AI.svg" alt="GitHub Pull Requests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue.svg" alt="License"></a>
</p>

---

<p align="center"> A multi-agent AI travel planner. Describe the trip you want in
    plain English and get back flights, hotels, weather and a day-by-day
    itinerary â€” researched for you in about a minute.
    <br>
</p>

## ðŸ“ Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Authors](#authors)
- [Acknowledgements](#acknowledgement)

## ðŸ§ About <a name = "about"></a>

Planning a trip usually means juggling half a dozen browser tabs â€” one for flights, another for hotels, a third for the weather, and a notes app where you try to fit it all into a sensible order. TripMind AI collapses that into a single conversation. You describe the trip you want in your own words, the way you'd describe it to a friend â€” *"Plan a 10 day Europe trip from India in April, mid-range budget"* â€” and a team of AI specialists goes and researches it. One looks into flights, another finds places to stay, another checks what the weather will be doing while you're there. Their findings are then pulled together into a single plan you can actually act on, complete with a day-by-day schedule and a cost estimate. The result is a trip plan in about a minute, rather than an afternoon of research. Each part of the trip gets its own attention:

| | |
|---|---|
| âœˆï¸ **Flights** | Likely airports, airlines on the route, typical duration and fare range |
| ðŸ¨ **Hotels** | Accommodation options matched to your destination and budget |
| ðŸŒ¤ï¸ **Weather** | Current conditions and the forecast, with travel advice |
| ðŸ—ºï¸ **Itinerary** | A realistic day-by-day plan you can actually follow |
| ðŸ’° **Budget** | An estimated breakdown of what the trip will cost |

Plans are saved as you go, so you can reopen a trip later and ask follow-up
questions without starting over.

## ðŸ Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your
local machine.

### Prerequisites

You'll need the following before you start:

- **Python 3.11**
- **[uv](https://docs.astral.sh/uv/)** â€” used to install dependencies
- **A PostgreSQL database** â€” a free [Render](https://render.com/) instance works fine
- **API keys** from the services below. All of them have free tiers:
  - [Groq](https://console.groq.com/)
  - [Tavily](https://tavily.com/)
  - [AviationStack](https://aviationstack.com/)
  - [OpenWeather](https://openweathermap.org/api)

### Installing

Clone the repository and move into it:

```bash
git clone https://github.com/Vishuu_Patil_001/TripMind-AI.git
cd TripMind-AI
```

Install the dependencies:

```bash
uv sync
```

Create a file named `.env` in the project root and add your keys:

```dotenv
# Required
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Service keys
TAVILY_API_KEY=your_tavily_key
AVIATIONSTACK_API_KEY=your_aviationstack_key
OPENWEATHER_API_KEY=your_openweather_key

# Optional
GROQ_MODEL=openai/gpt-oss-20b
```

Here's what each one is for:

| Variable | Required | What it's for |
|---|:---:|---|
| `GROQ_API_KEY` | âœ… | Powers the AI planning |
| `DATABASE_URL` | âœ… | Saves your trips so you can return to them |
| `TAVILY_API_KEY` | âœ… | Hotel search |
| `AVIATIONSTACK_API_KEY` | âœ… | Airport and airline information |
| `OPENWEATHER_API_KEY` | âœ… | Weather and forecasts |
| `GROQ_MODEL` | âŒ | Switch the AI model without editing any code |

Your `.env` file is ignored by Git. Never commit real keys.

Now start the app:

```bash
uv run python app.py
```

Open **<http://127.0.0.1:8000>** in your browser. If you see the planner with a
green *API connected* dot at the bottom of the sidebar, you're ready to go.

## ðŸŽˆ Usage <a name="usage"></a>

### Planning a trip

Type your request into the box at the bottom of the screen and press **Enter**.
Anything conversational works:

> Plan a 10 day Europe trip from India in April, mid-range budget

> I want a relaxed 5 day trip to Rome and Florence in September for two people

Not sure where to start? Click one of the suggestion cards on the home screen.

A plan takes **30â€“90 seconds** to build, and you'll see each stage as it
progresses.

### Using the trip builder

If you'd rather fill in fields than write a sentence, click the **sliders icon**
to the left of the message box. Enter your origin, destination, dates, duration,
number of travellers and budget, pick the things you're interested in, then hit
**Write my prompt**. Your request is composed for you, ready to send or edit.

### Reading your plan

Your results are split into tabs so you can jump straight to what you need:

**Plan** Â· **Itinerary** Â· **Flights** Â· **Hotels** Â· **Weather**

### Saving, exporting and revisiting

- Every trip is saved to the sidebar automatically â€” click any one to reopen it
- Ask follow-up questions on an open trip and it remembers the context
- Use the icons at the top of a result to **copy**, **download as Markdown** or **print**
- Click **New trip** to start fresh
- Switch between **light and dark mode** with the sun/moon icon at the bottom of the sidebar

## ðŸ¤” Troubleshooting <a name = "troubleshooting"></a>

<details>
<summary><b>The page loads but planning fails</b></summary>

Check the status indicator at the bottom of the sidebar. If it says *API
unreachable*, the app has stopped â€” restart it with `uv run python app.py`.
Otherwise, check the terminal you started the app in for the error.
</details>

<details>
<summary><b>An error says the model does not exist</b></summary>

AI providers retire models over time. List the ones your key can use:

```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

Pick one from the list and set it as `GROQ_MODEL` in your `.env` file.
</details>

<details>
<summary><b>An error says DATABASE_URL is missing</b></summary>

The app needs a PostgreSQL database to save your trips. Add a connection string
to your `.env` file â€” see [Installing](#getting_started).
</details>

<details>
<summary><b>Plans take a long time</b></summary>

This is expected. Several specialists research your trip in turn, and each step
involves live data and AI calls. 30â€“90 seconds is normal.
</details>

## ðŸ¤ Contributing <a name = "contributing"></a>

Contributions are welcome. This project is actively being developed, so there's
plenty to pick up.

### Getting set up

1. **Fork** the repository and clone your fork
2. Follow [Getting Started](#getting_started) to install everything
3. Create a branch for your work:

```bash
git checkout -b feature/your-feature-name
```

### Making your changes

- Keep each pull request focused on one thing
- Match the style of the code around you
- Check the app still runs end to end before you open a pull request
- Never commit your `.env` file or any API keys

### Submitting your work

Commit with a message that says what changed and why:

```bash
git commit -m "Add support for multi-city trips"
```

Push to your fork:

```bash
git push origin feature/your-feature-name
```

Then open a **pull request** against `main` describing what you changed, why,
and how you tested it.

### Reporting bugs and suggesting ideas

Open an [issue](https://github.com/Vishuu_Patil_001/TripMind-AI/issues).
For bugs, include what you did, what you expected, what happened instead, and
any error output from the terminal.

## ðŸŽ‰ Acknowledgements <a name = "acknowledgement"></a>

- [Groq](https://groq.com/) for fast AI inference
- [Tavily](https://tavily.com/), [AviationStack](https://aviationstack.com/) and
  [OpenWeather](https://openweathermap.org/) for the live travel data

---

Licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE).





