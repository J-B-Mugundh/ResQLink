import streamlit as st
import re
from math import radians, sin, cos, sqrt, atan2
import google.generativeai as genai

# ✅ Configure Gemini Client
genai.configure(api_key="AIzaSyAqPYE72UoSojB5KewKPYTpelAsYaoDIF8")

PRESET_LOCATIONS = {
    "Tambaram": (12.9229, 80.1275),
    "Chennai Central": (13.0827, 80.2707),
    "Kanchipuram": (12.8342, 79.7036)
}

def get_required_speciality(message):
    prompt = (
        "You are an AI that classifies emergencies into response categories. "
        "Given an emergency description, respond strictly with one of these words: "
        "'medical', 'firefighter', or 'general'. No explanations, no extra words, just the category.\n\n"
        f"Emergency description: {message}\n\n"
        "Response:"
    )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        match = re.search(r'\b(medical|firefighter|general)\b', text_response.lower())
        return match.group(1) if match else "general"
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "general"

def haversine(coord1, coord2):
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c  # Earth radius in km

def assign_responders(task, responders, radius_km=5):
    if task["severity"] == 0:
        return "Hello there, hope you are safe. ResQLink is working great!"

    required_speciality = get_required_speciality(task["message"])
    num_required = 2 if task["severity"] == 3 else 1
    assigned = []

    for responder in responders:
        if responder["speciality"] == required_speciality:
            for t in responder["assigned_tasks"]:
                if haversine(task["gps"], t) <= radius_km and responder not in assigned:
                    assigned.append(responder)
                    break

    available = [r for r in responders if r["speciality"] == required_speciality and r not in assigned]
    available.sort(key=lambda r: haversine(task["gps"], r["location"]))

    for responder in available:
        if len(assigned) >= num_required:
            break
        assigned.append(responder)

    for r in assigned:
        r["assigned_tasks"].append(task["gps"])
    return assigned

# Streamlit UI
st.title("ResQLink: Disaster Management System")

emergency_message = st.text_area("Enter emergency details:")
location_choice = st.selectbox("Select a location or enter manually:", ["Enter Manually"] + list(PRESET_LOCATIONS.keys()))

if location_choice == "Enter Manually":
    latitude = st.number_input("Enter latitude:", format="%.6f")
    longitude = st.number_input("Enter longitude:", format="%.6f")
else:
    latitude, longitude = PRESET_LOCATIONS[location_choice]

severity = st.selectbox("Select severity (0-Test, 1-Low, 2-Medium, 3-High):", [0, 1, 2, 3])

if st.button("Assign Responder"):
    if severity == 0:
        st.write("Hello there, hope you are safe. ResQLink is working great!")
    elif emergency_message and latitude and longitude:
        task = {"message": emergency_message, "gps": (latitude, longitude), "severity": severity}
        
        responders = [
            {"id": 1, "name": "Alice", "speciality": "medical", "location": (12.7041, 79.1025), "assigned_tasks": []},
            {"id": 2, "name": "Bob", "speciality": "firefighter", "location": (28.5355, 77.3910), "assigned_tasks": []},
            {"id": 3, "name": "Charlie", "speciality": "general", "location": (28.4595, 77.0266), "assigned_tasks": []},
            {"id": 4, "name": "David", "speciality": "medical", "location": (13.4089, 78.3178), "assigned_tasks": []},
            {"id": 5, "name": "Eve", "speciality": "firefighter", "location": (28.5355, 77.3910), "assigned_tasks": []},
            {"id": 6, "name": "Frank", "speciality": "general", "location": (28.4595, 77.0266), "assigned_tasks": []},
            {"id": 7, "name": "Grace", "speciality": "medical", "location": (28.7041, 77.1025), "assigned_tasks": []},
            {"id": 8, "name": "Heidi", "speciality": "firefighter", "location": (28.4089, 77.3178), "assigned_tasks": []},
            {"id": 9, "name": "Ivan", "speciality": "general", "location": (28.5355, 77.3910), "assigned_tasks": []},
            {"id": 10, "name": "Judy", "speciality": "medical", "location": (28.4595, 77.0266), "assigned_tasks": []},
            {"id": 11, "name": "Karl", "speciality": "firefighter", "location": (28.7041, 77.1025), "assigned_tasks": []},
            {"id": 12, "name": "Leo", "speciality": "general", "location": (28.4089, 77.3178), "assigned_tasks": []},
            {"id": 13, "name": "Mallory", "speciality": "medical", "location": (28.5355, 77.3910), "assigned_tasks": []},
            {"id": 14, "name": "Nancy", "speciality": "firefighter", "location": (28.4595, 77.0266), "assigned_tasks": []},
            {"id": 15, "name": "Oliver", "speciality": "general", "location": (28.7041, 77.1025), "assigned_tasks": []},
            {"id": 16, "name": "Peggy", "speciality": "medical", "location": (28.4089, 77.3178), "assigned_tasks": []},
            {"id": 17, "name": "Dr. Rajesh", "speciality": "medical", "location": (12.9249, 80.1278), "assigned_tasks": []},
            {"id": 18, "name": "Dr. Priya", "speciality": "medical", "location": (13.0675, 80.2376), "assigned_tasks": []},
            {"id": 19, "name": "Dr. Arjun", "speciality": "medical", "location": (12.9865, 80.2211), "assigned_tasks": []},
            {"id": 20, "name": "Karthik", "speciality": "firefighter", "location": (13.0825, 80.2706), "assigned_tasks": []},
            {"id": 21, "name": "Vijay", "speciality": "firefighter", "location": (12.8375, 79.7038), "assigned_tasks": []},
            {"id": 22, "name": "Suresh", "speciality": "firefighter", "location": (13.0415, 80.2337), "assigned_tasks": []},
            {"id": 23, "name": "Ramesh", "speciality": "general", "location": (12.9220, 80.1260), "assigned_tasks": []},
            {"id": 24, "name": "Sunita", "speciality": "general", "location": (13.0986, 80.2451), "assigned_tasks": []}
        ]

        assigned = assign_responders(task, responders)
        if isinstance(assigned, str):
            st.write(assigned)
        else:
            st.write("### Assigned Responders:")
            for responder in assigned:
                st.write(f"- {responder['name']} ({responder['speciality']}) at {responder['location']}")
    else:
        st.write("Please enter emergency details and valid coordinates.")
