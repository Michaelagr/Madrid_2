import streamlit as st
import json
from datetime import datetime, timedelta
import random

# App configuration
st.set_page_config(
    page_title="Madrid Reiseplan",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Madrid Trip Planner - Erstellt mit ♥️"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main .block-container {padding-top: 2rem;}
    .activity-item {background-color: #f9f9f9; border-radius: 5px; padding: 0.5rem; margin-bottom: 0.5rem;}
    .activity-controls {display: flex; justify-content: flex-end;}
    .custom-emoji {font-size: 1.2rem; margin-right: 0.5rem;}
    .stButton>button {margin-right: 0.2rem;}
    .stExpander {border-radius: 8px; overflow: hidden;}
    .section-header {font-weight: bold;}
    div[data-testid="stSidebarNav"] {background-image: url("https://cdn.pixabay.com/photo/2019/09/11/18/09/spain-4469698_1280.jpg"); background-size: cover; padding-top: 40px; background-position: center;}
    div.stButton > button:first-child {background-color: #ff9d5c; color:white; border:none;}
    div.stButton > button:hover {background-color: #ff7b2c; color:white; border:none;}
    .weather-box {padding: 10px; border-radius: 5px; background-color: #f0f8ff; margin-bottom: 15px;}
    .highlight {background-color: #ffffcc; padding: 0.2rem; border-radius: 3px;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for the itinerary data
if 'itinerary' not in st.session_state:
    default_itinerary = {
        "Tag 1 - Donnerstag – Klassiker & Altstadt": {
            "Frühstück": [
                {"text": "☕ *Café de la Luz* oder *HanSo Café* (Malasaña, 10 Minuten zu Fuß vom Hotel)", "emoji": "☕"}
            ],
            "Vormittag": [
                {"text": "📍 Puerta del Sol – das Herz Madrids", "emoji": "📍"},
                {"text": "🧭 Plaza Mayor – kurzer Stopp bei *Chocolatería San Ginés* für Churros", "emoji": "🧭"}
            ],
            "Mittagessen": [
                {"text": "🍤 Mercado de San Miguel – Tapas von verschiedenen Ständen", "emoji": "🍤"},
                {"text": "🍽️ Alternativ: *Casa Revuelta* – legendärer Bacalao", "emoji": "🍽️"}
            ],
            "Nachmittag": [
                {"text": "🏛️ Almudena-Kathedrale & Palacio Real", "emoji": "🏛️"},
                {"text": "🌳 Pause in den Gärten *Sabatini* oder *Campo del Moro*", "emoji": "🌳"}
            ],
            "Abendessen": [
                {"text": "🍹 Rooftop-Aperitif: *Picalagartos* oder *Doña Luz*", "emoji": "🍹"},
                {"text": "🍷 Abendessen: *La Taberna de Elia* (klassisch & lokal)", "emoji": "🍷"}
            ]
        },
        "Tag 2 - Freitag": {
            "Frühstück": [
                {"text": "☕ *Café de Oriente* oder *Federal Café*", "emoji": "☕"}
            ],
            "Vormittag": [
                {"text": "🖼️ Besuch im *Museo del Prado* oder *Reina Sofía* (für Picasso & Co.)", "emoji": "🖼️"}
            ],
            "Mittagessen": [
                {"text": "🍷 *Los Gatos* oder *Bodega de los Secretos* (stylische Location!)", "emoji": "🍷"}
            ],
            "Nachmittag": [
                {"text": "🌿 Spaziergang durch den *Retiro-Park* mit Kristallpalast", "emoji": "🌿"},
                {"text": "📖 Bummel durchs *Barrio de las Letras* (literarisches Viertel)", "emoji": "📖"}
            ],
            "Abendessen": [
                {"text": "🍷 *La Venencia* – authentisch, Sherry-Bar, keine Fotos erlaubt", "emoji": "🍷"},
                {"text": "🥘 Alternativ: *Inclán Brutal* – kreative Tapas", "emoji": "🥘"}
            ]
        },
        "Tag 3 - Samstag": {
            "Frühstück": [
                {"text": "☕ *Plántate Café* oder *The Fix* (Lavapiés)", "emoji": "☕"}
            ],
            "Vormittag": [
                {"text": "🎨 Erkundung von *Lavapiés*: Street Art, kleine Galerien, alternative Läden", "emoji": "🎨"}
            ],
            "Mittagessen": [
                {"text": "🍽️ *Mercado de Antón Martín* – vielfältige Auswahl", "emoji": "🍽️"}
            ],
            "Nachmittag": [
                {"text": "🚶 Spaziergang durch *La Latina* mit Plaza de la Paja", "emoji": "🚶"},
                {"text": "🏛️ Optional: *Museo Cerralbo* – ein echter Geheimtipp!", "emoji": "🏛️"}
            ],
            "Abendessen": [
                {"text": "🔥 *Sobrino de Botín* – ältestes Restaurant der Welt (vorher reservieren!)", "emoji": "🔥"},
                {"text": "🍷 Alternativ: *Taberna Tempranillo* auf der *Cava Baja*", "emoji": "🍷"}
            ]
        },
        "Tag 4 - Sonntag": {
            "Frühstück": [
                {"text": "☕ *El Jardín Secreto* oder Hotelfrühstück auf der Terrasse", "emoji": "☕"}
            ],
            "Vormittag": [
                {"text": "🛍️ Bummel über die *Gran Vía*, Shopping oder Cafébesuch", "emoji": "🛍️"},
                {"text": "🌇 Rooftop: *Círculo de Bellas Artes* (fantastischer Ausblick!)", "emoji": "🌇"}
            ],
            "Mittagessen": [
                {"text": "🥘 *Lamucca de Pez* oder *Toma Jamón*", "emoji": "🥘"}
            ],
            "Nachmittag": [
                {"text": "🕌 *Templo de Debod* – ägyptischer Tempel mit Sonnenuntergang", "emoji": "🕌"},
                {"text": "🖼️ Optional: *Museo Sorolla* (klein & ruhig)", "emoji": "🖼️"}
            ],
            "Abendessen": [
                {"text": "🌿 *Botania* (gleich beim Hotel, stilvoll)", "emoji": "🌿"},
                {"text": "🍄 *El Cisne Azul* – für Pilzliebhaber", "emoji": "🍄"}
            ]
        },
        "Tag 5 - Montag - Abreise": {
            "Abflug": [
                {"text": "✈️ 6.20 Uhr Madrid Flughafen", "emoji": "✈️"}
            ]
        }
    }
    st.session_state.itinerary = default_itinerary

    # Default trip settings
    st.session_state.trip_settings = {
        "start_date": datetime.now() + timedelta(days=30),
        "end_date": datetime.now() + timedelta(days=34),
        "hotel": "Gran Vía 21, Madrid",
        "trip_name": "Madrid Reiseplan",
        "trip_description": "Für unsere Reise ♥️ – mit viel Zeit für gutes Essen, Entspannung und Genuss."
    }

    # Default common timeslots for all days
    st.session_state.default_timeslots = [
        "Frühstück", "Vormittag", "Mittagessen", "Nachmittag", "Abendessen"
    ]

    # List of common emojis for activities
    st.session_state.activity_emojis = [
        "☕", "🍽️", "🏛️", "🖼️", "🌳", "🚶", "🍷", "🍹", "🥘", "🌇",
        "📍", "🧭", "🎨", "🍤", "🛍️", "📖", "🔥", "🕌", "🌿", "🍄", "✈️"
    ]

    # Weather forecast (simulated data)
    st.session_state.weather = {
        "Tag 1 - Donnerstag – Klassiker & Altstadt": {"icon": "☀️", "temp": "28°C", "desc": "Sonnig"},
        "Tag 2 - Freitag": {"icon": "⛅", "temp": "26°C", "desc": "Teilweise bewölkt"},
        "Tag 3 - Samstag": {"icon": "☀️", "temp": "29°C", "desc": "Sonnig"},
        "Tag 4 - Sonntag": {"icon": "🌦️", "temp": "25°C", "desc": "Vereinzelt Regen"},
        "Tag 5 - Montag - Abreise": {"icon": "☀️", "temp": "27°C", "desc": "Sonnig"}
    }


# Functions for itinerary management
def update_day_name(old_name, new_name):
    """Update a day's name and keep the content"""
    if old_name != new_name and new_name not in st.session_state.itinerary:
        st.session_state.itinerary[new_name] = st.session_state.itinerary.pop(old_name)
        st.session_state.weather[new_name] = st.session_state.weather.pop(old_name, {"icon": "☀️", "temp": "25°C",
                                                                                     "desc": "Sonnig"})
        return True
    return False


def add_new_day():
    """Add a new day to the itinerary"""
    new_day = f"Tag {len(st.session_state.itinerary) + 1} - Neu"
    if new_day not in st.session_state.itinerary:
        st.session_state.itinerary[new_day] = {}
        for section in st.session_state.default_timeslots:
            st.session_state.itinerary[new_day][section] = []
        st.session_state.weather[new_day] = {"icon": "☀️", "temp": "25°C", "desc": "Sonnig"}
        return new_day
    return None


def delete_day(day_name):
    """Delete a day from the itinerary"""
    if day_name in st.session_state.itinerary:
        del st.session_state.itinerary[day_name]
        if day_name in st.session_state.weather:
            del st.session_state.weather[day_name]
        return True
    return False


def add_section(day, section_name):
    """Add new section to a day"""
    if day in st.session_state.itinerary and section_name:
        if section_name not in st.session_state.itinerary[day]:
            st.session_state.itinerary[day][section_name] = []
            return True
    return False


def delete_section(day, section_name):
    """Delete section from a day"""
    if day in st.session_state.itinerary and section_name in st.session_state.itinerary[day]:
        del st.session_state.itinerary[day][section_name]
        return True
    return False


def add_activity(day, section, activity_text, emoji="📌"):
    """Add activity to a section"""
    if day in st.session_state.itinerary and section in st.session_state.itinerary[day]:
        st.session_state.itinerary[day][section].append({"text": f"{emoji} {activity_text}", "emoji": emoji})
        return True
    return False


def delete_activity(day, section, activity_index):
    """Delete activity from a section"""
    if (day in st.session_state.itinerary and
            section in st.session_state.itinerary[day] and
            0 <= activity_index < len(st.session_state.itinerary[day][section])):
        del st.session_state.itinerary[day][section][activity_index]
        return True
    return False


def move_activity_up(day, section, activity_index):
    """Move activity up in the list"""
    if (day in st.session_state.itinerary and
            section in st.session_state.itinerary[day] and
            0 < activity_index < len(st.session_state.itinerary[day][section])):
        activities = st.session_state.itinerary[day][section]
        activities[activity_index], activities[activity_index - 1] = activities[activity_index - 1], activities[
            activity_index]
        return True
    return False


def move_activity_down(day, section, activity_index):
    """Move activity down in the list"""
    if (day in st.session_state.itinerary and
            section in st.session_state.itinerary[day] and
            0 <= activity_index < len(st.session_state.itinerary[day][section]) - 1):
        activities = st.session_state.itinerary[day][section]
        activities[activity_index], activities[activity_index + 1] = activities[activity_index + 1], activities[
            activity_index]
        return True
    return False


def move_section_up(day, section_name):
    """Move a section up in the day's order"""
    if day in st.session_state.itinerary:
        sections = list(st.session_state.itinerary[day].keys())
        if section_name in sections and sections.index(section_name) > 0:
            idx = sections.index(section_name)
            new_order = {}
            for i, section in enumerate(sections):
                if i == idx - 1:
                    new_order[section_name] = st.session_state.itinerary[day][section_name]
                    new_order[sections[idx - 1]] = st.session_state.itinerary[day][sections[idx - 1]]
                elif i != idx:
                    new_order[section] = st.session_state.itinerary[day][section]
            st.session_state.itinerary[day] = new_order
            return True
    return False


def move_section_down(day, section_name):
    """Move a section down in the day's order"""
    if day in st.session_state.itinerary:
        sections = list(st.session_state.itinerary[day].keys())
        if section_name in sections and sections.index(section_name) < len(sections) - 1:
            idx = sections.index(section_name)
            new_order = {}
            for i, section in enumerate(sections):
                if i == idx + 1:
                    new_order[sections[idx + 1]] = st.session_state.itinerary[day][sections[idx + 1]]
                    new_order[section_name] = st.session_state.itinerary[day][section_name]
                elif i != idx:
                    new_order[section] = st.session_state.itinerary[day][section]
            st.session_state.itinerary[day] = new_order
            return True
    return False


def update_weather(day, icon, temp, desc):
    """Update weather information for a day"""
    if day in st.session_state.weather:
        st.session_state.weather[day] = {"icon": icon, "temp": temp, "desc": desc}
        return True
    return False


def export_itinerary():
    """Export the itinerary as JSON"""
    return json.dumps(st.session_state.itinerary, indent=2, ensure_ascii=False)


def import_itinerary(json_data):
    """Import an itinerary from JSON"""
    try:
        data = json.loads(json_data)
        st.session_state.itinerary = data
        return True
    except:
        return False


def update_itinerary_name_and_desc(name, desc):
    """Update the itinerary name and description"""
    st.session_state.trip_settings["trip_name"] = name
    st.session_state.trip_settings["trip_description"] = desc


def random_emoji():
    """Return a random emoji from the list"""
    return random.choice(st.session_state.activity_emojis)


# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn.pixabay.com/photo/2018/01/31/05/43/panoramic-3120484_1280.jpg", use_container_width=True)

    # Trip settings expander
    with st.expander("⚙️ Trip-Einstellungen", expanded=False):
        # Trip name and description
        trip_name = st.text_input("Reisename", st.session_state.trip_settings["trip_name"])
        trip_desc = st.text_area("Beschreibung", st.session_state.trip_settings["trip_description"])

        if st.button("Aktualisieren", key="update_trip_info"):
            update_itinerary_name_and_desc(trip_name, trip_desc)
            st.success("Trip-Informationen aktualisiert!")

        # Date settings
        start_date = st.date_input("Startdatum", st.session_state.trip_settings["start_date"])
        end_date = st.date_input("Enddatum", st.session_state.trip_settings["end_date"])

        if start_date and end_date:
            st.session_state.trip_settings["start_date"] = start_date
            st.session_state.trip_settings["end_date"] = end_date

        # Hotel information
        hotel = st.text_input("Hotel/Unterkunft", st.session_state.trip_settings["hotel"])
        st.session_state.trip_settings["hotel"] = hotel

    # Export/Import functionality
    with st.expander("📤 Export/Import", expanded=False):
        if st.button("Reiseplan exportieren"):
            st.download_button(
                label="JSON herunterladen",
                data=export_itinerary(),
                file_name="madrid_trip.json",
                mime="application/json"
            )

        uploaded_file = st.file_uploader("Reiseplan importieren", type="json")
        if uploaded_file is not None:
            json_data = uploaded_file.read().decode("utf-8")
            if import_itinerary(json_data):
                st.success("Reiseplan erfolgreich importiert!")
            else:
                st.error("Fehler beim Importieren des Reiseplans.")

    # Day navigation
    st.markdown("### 📅 Tagesplan wählen")

    # Add new day button
    if st.button("+ Neuen Tag hinzufügen", key="add_day_btn"):
        new_day = add_new_day()
        if new_day:
            st.success(f"Tag '{new_day}' hinzugefügt!")

    # Day selection with radio buttons
    days = list(st.session_state.itinerary.keys())
    selected_day = st.radio("", days, label_visibility="collapsed")

    # Show edit mode toggle
    edit_mode = st.checkbox("✏️ Bearbeitungsmodus", value=False)

    st.markdown("---")
    st.info("✨ Auf einen wundervollen Trip! Ich freue mich sehr ♥️")

# Main content area
st.title(f"🌆 {st.session_state.trip_settings['trip_name']}")
st.markdown(f"**{st.session_state.trip_settings['trip_description']}**")

# Display hotel information
cols = st.columns([3, 1])
with cols[0]:
    st.markdown(f"**🏨 Unterkunft:** {st.session_state.trip_settings['hotel']}")
with cols[1]:
    start = st.session_state.trip_settings["start_date"].strftime("%d.%m")
    end = st.session_state.trip_settings["end_date"].strftime("%d.%m.%Y")
    st.markdown(f"**📆 Reisezeitraum:** {start} - {end}")

# Day header and weather
day_header_cols = st.columns([3, 1])
with day_header_cols[0]:
    if edit_mode:
        new_day_name = st.text_input("Tag bearbeiten", selected_day, key=f"edit_day_{selected_day}")
        if st.button("Umbenennen", key=f"rename_day_{selected_day}"):
            if update_day_name(selected_day, new_day_name):
                st.success(f"Tag umbenannt zu '{new_day_name}'!")
                st.rerun()
            else:
                st.error("Der Name existiert bereits oder ist ungültig.")

        if st.button("Tag löschen", key=f"delete_day_{selected_day}"):
            if delete_day(selected_day):
                st.warning(f"Tag '{selected_day}' gelöscht!")
                st.rerun()
    else:
        st.header(selected_day)

with day_header_cols[1]:
    weather = st.session_state.weather.get(selected_day, {"icon": "☀️", "temp": "25°C", "desc": "Sonnig"})

    if edit_mode:
        # Weather editing
        weather_cols = st.columns(3)
        with weather_cols[0]:
            icon = st.selectbox("Icon", ["☀️", "⛅", "🌦️", "🌧️", "⛈️", "❄️"],
                                index=["☀️", "⛅", "🌦️", "🌧️", "⛈️", "❄️"].index(weather["icon"]))
        with weather_cols[1]:
            temp = st.text_input("Temp", weather["temp"])
        with weather_cols[2]:
            desc = st.text_input("Desc", weather["desc"])

        if st.button("Wetter aktualisieren"):
            update_weather(selected_day, icon, temp, desc)
            st.success("Wetter aktualisiert!")
    else:
        st.markdown(f"""
        <div class="weather-box">
            <h3>{weather['icon']} {weather['temp']}</h3>
            <p>{weather['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# Display sections for the selected day
day_plan = st.session_state.itinerary[selected_day]

# Add new section (only in edit mode)
if edit_mode:
    st.markdown("### Abschnitt hinzufügen")
    new_section_cols = st.columns([3, 1])
    with new_section_cols[0]:
        new_section_name = st.text_input("Neuer Abschnitt", key="new_section_input")
    with new_section_cols[1]:
        if st.button("Hinzufügen", key="add_section_btn"):
            if add_section(selected_day, new_section_name):
                st.success(f"Abschnitt '{new_section_name}' hinzugefügt!")
                st.rerun()
            else:
                st.error("Der Abschnitt existiert bereits oder ist ungültig.")

# Display each section
for section, items in day_plan.items():
    with st.expander(f"**{section}**", expanded=True):
        # Section controls (only in edit mode)
        if edit_mode:
            section_controls = st.columns([1, 1, 1, 1])
            with section_controls[0]:
                if st.button("↑", key=f"move_up_{section}"):
                    if move_section_up(selected_day, section):
                        st.rerun()
            with section_controls[1]:
                if st.button("↓", key=f"move_down_{section}"):
                    if move_section_down(selected_day, section):
                        st.rerun()
            with section_controls[2]:
                if st.button("Umbenennen", key=f"rename_{section}"):
                    st.session_state[f"rename_section_{section}"] = True
            with section_controls[3]:
                if st.button("Löschen", key=f"delete_{section}"):
                    if delete_section(selected_day, section):
                        st.success(f"Abschnitt '{section}' gelöscht!")
                        st.rerun()

        # Section rename form (only shown when rename button is clicked)
        if edit_mode and st.session_state.get(f"rename_section_{section}", False):
            rename_col1, rename_col2 = st.columns([3, 1])
            with rename_col1:
                new_section_name = st.text_input("Neuer Name", section, key=f"new_name_{section}")
            with rename_col2:
                if st.button("Speichern", key=f"save_name_{section}"):
                    if add_section(selected_day, new_section_name):
                        st.session_state.itinerary[selected_day][new_section_name] = st.session_state.itinerary[
                            selected_day].pop(section)
                        st.session_state[f"rename_section_{section}"] = False
                        st.success(f"Abschnitt umbenannt zu '{new_section_name}'!")
                        st.rerun()
                    else:
                        st.error("Der Name existiert bereits oder ist ungültig.")

        # Display items in the section
        for i, item in enumerate(items):
            item_text = item["text"]

            if edit_mode:
                cols = st.columns([3, 1, 1, 1, 1])
                with cols[0]:
                    st.markdown(item_text)
                with cols[1]:
                    if st.button("↑", key=f"up_{section}_{i}"):
                        if move_activity_up(selected_day, section, i):
                            st.rerun()
                with cols[2]:
                    if st.button("↓", key=f"down_{section}_{i}"):
                        if move_activity_down(selected_day, section, i):
                            st.rerun()
                with cols[3]:
                    if st.button("✏️", key=f"edit_{section}_{i}"):
                        st.session_state[f"edit_activity_{section}_{i}"] = True
                with cols[4]:
                    if st.button("🗑️", key=f"delete_{section}_{i}"):
                        if delete_activity(selected_day, section, i):
                            st.success("Aktivität gelöscht!")
                            st.rerun()
            else:
                st.markdown(f"- {item_text}")

            # Activity edit form
            if edit_mode and st.session_state.get(f"edit_activity_{section}_{i}", False):
                edit_cols = st.columns([1, 3, 1])
                with edit_cols[0]:
                    emoji = st.selectbox("Emoji", st.session_state.activity_emojis,
                                         index=st.session_state.activity_emojis.index(item["emoji"]) if item[
                                                                                                            "emoji"] in st.session_state.activity_emojis else 0,
                                         key=f"emoji_{section}_{i}")
                with edit_cols[1]:
                    # Extract text without emoji
                    text = item_text
                    if item["emoji"] in item_text:
                        text = item_text[len(item["emoji"]):].strip()
                    activity_text = st.text_input("Aktivität", text, key=f"text_{section}_{i}")
                with edit_cols[2]:
                    if st.button("Speichern", key=f"save_{section}_{i}"):
                        st.session_state.itinerary[selected_day][section][i] = {"text": f"{emoji} {activity_text}",
                                                                                "emoji": emoji}
                        st.session_state[f"edit_activity_{section}_{i}"] = False
                        st.success("Aktivität aktualisiert!")
                        st.rerun()

        # Add activity form (only in edit mode)
        if edit_mode:
            st.markdown("---")
            add_cols = st.columns([1, 3, 1])
            with add_cols[0]:
                new_emoji = st.selectbox("Emoji", st.session_state.activity_emojis, key=f"new_emoji_{section}")
            with add_cols[1]:
                new_activity = st.text_input("Neue Aktivität", "", key=f"new_activity_{section}")
            with add_cols[2]:
                if st.button("Hinzufügen", key=f"add_to_{section}"):
                    if add_activity(selected_day, section, new_activity, new_emoji):
                        st.success("Aktivität hinzugefügt!")
                        st.rerun()
                    else:
                        st.error("Fehler beim Hinzufügen der Aktivität.")

# Add map at the bottom
st.markdown("---")
st.subheader("📍 Karte")
st.markdown("Hier sind alle Orte auf der Karte")
