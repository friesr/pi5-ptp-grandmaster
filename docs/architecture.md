# System Architecture

The system is composed of four major layers:

1. **Backend (Flask)**  
   Provides APIs for GNSS, NTP, PTP, system metrics, configuration, and storage.

2. **Frontend (HTML/CSS/JS)**  
   A dark-themed dashboard with live updates and configuration controls.

3. **System Layer (systemd + install script)**  
   Ensures the dashboard runs automatically and integrates with PTP services.

4. **Data Layer**  
   Local and NAS storage with rolling archives and Excel export.

A full architecture diagram will be added once the Pi hardware is online.
