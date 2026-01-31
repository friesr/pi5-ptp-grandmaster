# Storage System

The system uses a two-tier storage model:

1. **Local Storage (`/opt/ptp-data/live`)**  
   Holds recent data up to a configurable size (default 20 GB).

2. **NAS Archive (`/opt/ptp-data/archive`)**  
   Stores long-term data up to a configurable size (default 200 GB).

A rolling archive process will automatically move older files from local to NAS.

Excel export will allow users to download processed data for analysis.
