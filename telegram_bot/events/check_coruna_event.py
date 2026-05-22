from datetime import datetime 


def check_event(event):

    if len(event) <= 1:
        return event[0]

    current_event = event[0]
    next_event = event [1]
    current_event_name = current_event["name"]["text"].strip().lower()
    next_event_name = next_event["name"]["text"].strip().lower()
    current_event_month = datetime.fromisoformat(current_event["start"]["local"]).month
    next_event_month = datetime.fromisoformat(next_event["start"]["local"]).month


    if current_event_name != next_event_name:
        return current_event
    
    if current_event_month == next_event_month:
        return next_event
    else:
        return current_event