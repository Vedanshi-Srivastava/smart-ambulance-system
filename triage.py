def classify_severity(text):
    text = text.lower()

    # Critical conditions
    critical_keywords = [
        "unconscious", "not breathing", "heart attack",
        "severe bleeding", "stroke", "accident", "critical"
    ]

    # Urgent conditions
    urgent_keywords = [
        "fracture", "bleeding", "injury",
        "high fever", "vomiting", "pain"
    ]

    # Check for critical
    for word in critical_keywords:
        if word in text:
            return "🔴 RED (Critical)"

    # Check for urgent
    for word in urgent_keywords:
        if word in text:
            return "🟠 ORANGE (Urgent)"

    # Default
    return "🟡 YELLOW (Stable)"