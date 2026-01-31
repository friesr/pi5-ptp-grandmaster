PTP_PROFILES = {
    "default": {
        "description": "Linux default PTP profile",
        "ptp4l": {
            "domainNumber": 0,
            "logAnnounceInterval": 1,
            "logSyncInterval": 0,
            "logMinDelayReqInterval": 0,
            "priority1": 128,
            "priority2": 128
        },
        "phc2sys": {
            "sync_interval": 1
        }
    },

    "g8275.1": {
        "description": "Telecom profile G.8275.1 (full timing support)",
        "ptp4l": {
            "domainNumber": 24,
            "logAnnounceInterval": -3,
            "logSyncInterval": -4,
            "logMinDelayReqInterval": -4,
            "priority1": 128,
            "priority2": 128,
            "transportSpecific": 0x1
        },
        "phc2sys": {
            "sync_interval": 0.5
        }
    },

    "g8275.2": {
        "description": "Telecom profile G.8275.2 (partial timing support)",
        "ptp4l": {
            "domainNumber": 24,
            "logAnnounceInterval": 0,
            "logSyncInterval": -3,
            "logMinDelayReqInterval": -3,
            "priority1": 128,
            "priority2": 128,
            "transportSpecific": 0x1
        },
        "phc2sys": {
            "sync_interval": 1
        }
    }
}
