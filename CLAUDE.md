# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 5G signal visualization dashboard challenge for the "Code with AI" contest. The goal is to build an interactive web dashboard using Streamlit to visualize 5G road test data.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run tests (when added)
pytest
```

## Data Structure

The `data/signal_samples.csv` contains 5G signal measurements with these columns:
- `Latitude`, `Longitude` - Geographic coordinates
- `CellID` - Cell tower ID
- `Band` - Frequency band (n28, n41, n78)
- `RSRP_dBm` - Signal strength in dBm (key metric for coloring)
- `SINR_dB` - Signal-to-interference-plus-noise ratio
- `TerminalType` - Device type (Smartphone, CPE, IoT)
- `Download_Mbps` - Download speed

## Contest Requirements

**Basic (Required):**
1. Load CSV data with pandas
2. Interactive map with latitude/longitude points, colored by RSRP_dBm (green > -90dBm, red < -110dBm)
3. Chart showing band distribution or terminal type breakdown

**Advanced (Bonus):**
1. Sidebar with filters (band dropdown, RSRP range slider) with real-time map/chart updates
2. 3D map with signal points as bars, height based on download speed
3. Code comments and unit tests

## Git Tags for Progress

- `git tag basic-done && git push origin basic-done` - Mark basic level complete
- `git tag advanced-done && git push origin advanced-done` - Mark advanced level complete