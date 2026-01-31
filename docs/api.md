# API Documentation

The backend exposes the following API groups:

- `/api/status/`  
  Returns GNSS, NTP, PTP, and system metrics.

- `/api/validation/status`  
  Returns validation indicators.

- `/api/storage/status`  
  Returns local and NAS storage usage.

- `/api/config/`  
  GET: returns configuration  
  POST: updates configuration

- `/api/export/excel`  
  Placeholder for Excel export.

More detailed schemas will be added as the samplers and validation logic are implemented.
