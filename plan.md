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
    <!-- not allow to add invalid tasks -->

### Achilles

Schema
    Tasks (__TID__, Name, Details, SID, DDate)
    Tags (__TID__, __Name__)
    Status (__SID__, Name)
    TT (__TaskID__, __TagID__)

Table
    Table Tasks (
        TID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(40) DEFAULT 'No-name' NOT NULL,
        Details VARCHAR(40) DEFAULT NULL,
        SID INTEGER,
        DDate DATETIME,
        FOREIGN KEY Status = Status.TID
    )

    Table Tags (
        TID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(40) PRIMARY KEY NOT NULL
    )

    Table Status (
        SID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(40) PRIMARY KEY NOT NULL
    )

    Table TT (
        TaskID INTEGER,
        TagID INTEGER,
        FOREIGN KEY TaskID = Task.TID, TagID = Tags.TID,
        PRIMARY KEY (TaskID + TagID)
    )


MAC: 2C:CF:67:14:6E:B7
IP: 192.168.31.122

Changes
    only list one table in index page to prevent dragging to other table
    save dragging order
    delete confirmation screen
    reset confirmation screen
    hyperlink retrn home page 
    calendar
