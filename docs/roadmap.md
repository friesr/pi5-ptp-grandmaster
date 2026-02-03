# Project Roadmap

## Phase 1 — Scaffold (Complete)
- Backend structure
- Frontend structure
- Systemd services
- Documentation framework

## Phase 2 — Core Functionality
- GNSS sampler
- NTP sampler
- PTP sampler
- Validation logic
- Storage manager

## Phase 3 — Visualization
- Offset charts
- Drift charts
- Allan deviation
- Satellite SNR charts

## Phase 4 — Hardware Integration
- PPS wiring
- GNSS receiver configuration
- PTP tuning

## Phase 5 — Release
- Full documentation
- Install images
- Public demo

Revisioned:

GNSS Timing Observatory — Full System Roadmap

A structured, milestone‑driven plan for building a complete GNSS/PTP/NTP timing observatory.

PHASE 1 — Backend Stability & API Alignment

Goal: Establish a clean, predictable backend with correct routing and reliable startup.

1.1 API Routing

Align blueprint prefixes with redirect logic.

Ensure /api/global/system/health resolves correctly.

Validate all endpoints using curl.

Add automated route self‑test on backend startup.

1.2 Backend Launch Procedure

Make PYTHONPATH injection permanent.

Standardize venv activation.

Use python -m backend.app as the canonical start method.

Add optional systemd service for automatic startup.

1.3 Logging & Diagnostics

Implement structured JSON logging.

Add rotating log files under /opt/ptp-data/logs.

Create a startup diagnostics endpoint.

PHASE 2 — GNSS + NTP Data Ingest Pipeline

Goal: Real‑time ingest of all timing‑critical data into a unified internal bus.

2.1 GNSS Ingest

Parse gpsd JSON.

Extract PPS, fix, SNR, constellation, jitter.

Normalize timestamps.

Push into GlobalIntelBus.

2.2 Chrony/NTP Ingest

Parse chronyc tracking and chronyc sources.

Extract offset, jitter, root dispersion, frequency.

Push into GlobalIntelBus.

2.3 System Metrics

Collect CPU temperature, load, drift, PPS stability.

Push into GlobalIntelBus.

2.4 Internal Data Contracts

Define schemas for gps_status, ntp_status, and system_metrics.

Add versioning for future compatibility.

PHASE 3 — Historical Storage (InfluxDB or Alternative)

Goal: Long‑term storage of timing data with retention, downsampling, and fast queries.

3.1 Database Selection

InfluxDB (recommended for Pi + high‑frequency data).

TimescaleDB (for SQL analytics).

VictoriaMetrics (for ultra‑low RAM usage).

3.2 Installation & Configuration

Install under /opt/influxdb.

Create buckets:

ptp_observatory_raw (90‑day retention).

ptp_observatory_downsampled (1‑year retention).

3.3 Backend → DB Writer

Add InfluxDB client.

Batch writes every 1 second.

Tag by satellite ID, constellation, NTP source, and stratum.

3.4 Retention & Downsampling

Raw: 1‑second resolution.

Downsampled: 1‑minute and 1‑hour rollups.

PHASE 4 — USNO + External Reference Integration

Goal: Enrich local timing data with authoritative national timing sources.

4.1 USNO Data Sources

UTC(USNO) – UTC offsets.

GPS‑UTC corrections.

Satellite health bulletins.

Earth Orientation Parameters (EOP).

Leap second announcements.

Bulletin A / Bulletin B.

4.2 Fetching & Parsing

Daily fetch job.

Parse into structured records.

Store in InfluxDB under:

usno_reference.

usno_eop.

usno_gps_offsets.

4.3 Cross‑Correlation

Compare local PPS vs USNO.

Detect drift and anomalies.

Improve timing confidence scoring.

PHASE 5 — Frontend Integration & Visualization

Goal: Provide a clean, operator‑ready UI for real‑time and historical intelligence.

5.1 Real‑Time Dashboard

System health.

GNSS constellation.

PPS jitter.

NTP discipline.

Clock offset.

Drift indicators.

5.2 Historical Views

GNSS SNR over time.

PPS jitter history.

NTP offset history.

CPU temperature vs drift correlation.

Satellite availability timeline.

5.3 Global Map (Future)

Node federation.

Constellation overlays.

Timing confidence heatmap.

PHASE 6 — Prediction, Simulation, and Alerts

Goal: Transform the observatory into an intelligent timing instrument.

6.1 Prediction Engine

Drift forecasting.

PPS stability prediction.

NTP source reliability scoring.

Satellite availability prediction.

6.2 Simulation Engine

Replay historical timing events.

Simulate GNSS outages.

Simulate multipath.

Simulate leap second events.

6.3 Alerts

Offset threshold violations.

PPS jitter spikes.

GNSS fix loss.

NTP source degradation.

USNO discrepancy detection.

PHASE 7 — Packaging & Deployment

Goal: Make the system reproducible, portable, and Pi‑ready.

7.1 Repository Structure

/backend.

/frontend.

/ptp-data.

/docs.

/deploy.

7.2 Install Script

One‑command install.

Creates venv.

Installs dependencies.

Configures InfluxDB.

Sets up systemd service.

7.3 Pi Image (Optional)

Prebuilt SD card image.

Fully configured observatory.

Plug‑and‑play deployment.

PHASE 8 — Federation & Global Intelligence (Long‑Term Vision)

Goal: Build a distributed network of timing observatories.

8.1 Node Identity

Unique node ID.

Public key.

Capability profile.

8.2 Secure Federation

Encrypted data exchange.

Peer discovery.

Shared timing intelligence.

8.3 Global Map

Real‑time node health.

Constellation overlays.

Drift anomalies.

Regional timing confidence.

This roadmap provides a complete, milestone‑driven plan for building a professional‑grade GNSS/PTP/NTP timing observatory. It is structured for GitHub documentation and ready for iterative implementation.
