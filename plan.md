Format
    Toggl
    HKOJ
    Notion

Function
    Tasks
    Report
    Verification

Plugins
    AI
    Login
    Calandar
    Report
    Accessible
    Music
    Timer

Reminder
    double confirm when deleting previous tasks
    add navigation bar
    not allow to add invalid tasks

### Achilles

Schema
    Task (__TID__, Name, Status)

Table
    Table Task (
        TID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(40) DEFAULT 'No-name' NOT NULL,
        Status BOOLEAN DEFAULT false
    )