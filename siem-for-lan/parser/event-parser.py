import win32evtlog
import pandas as pd

# Log types include : System, Application, Security, Setup
def get_event_logs(log_type="System", max_events=100):
    logs = []
    hand = win32evtlog.OpenEventLog(None, log_type)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    
    count = 0
    for event in events:
        if count >= max_events:
            break
        logs.append({
            "Time": event.TimeGenerated.Format(),
            "Source": event.SourceName,
            "Event ID": event.EventID,
            "Category": event.EventCategory,
            "Message": event.StringInserts
        })
        count += 1

    win32evtlog.CloseEventLog(hand)
    return logs

# Convert to DataFrame and save to Excel
logs = get_event_logs("System", 100)
df = pd.DataFrame(logs)
df.to_excel("Windows_Logs.xlsx", index=False)

print("Logs exported to Windows_Logs.xlsx")
