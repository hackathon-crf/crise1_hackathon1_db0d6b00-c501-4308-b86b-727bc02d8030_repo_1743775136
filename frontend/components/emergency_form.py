import streamlit as st
# from streamlit_javascript import st_javascript
import streamlit.components.v1 as components
import requests
import geocoder

def get_fallback_location():
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        st.success(f"📍 Position détectée via navigateur : {g.latlng[0]}, {g.latlng[1]}")
        return g.latlng[0], g.latlng[1]
    return None, None


def get_user_location():
    """
    Try browser geolocation, fallback to IP-based location, then manual address.
    Returns (lat, lon) or (None, None)
    """

#     coords_placeholder = st.empty()

# # Create an iframe-based JS component
#     components.html(
#         """
#         <script>
#         const sendPositionToStreamlit = (lat, lon) => {
#             const streamlitChannel = parent.postMessage({ isStreamlitMessage: true, type: 'geo', lat: lat, lon: lon }, '*');
#         };

#         navigator.geolocation.getCurrentPosition(
#             position => {
#                 const lat = position.coords.latitude;
#                 const lon = position.coords.longitude;
#                 sendPositionToStreamlit(lat, lon);
#             },
#             error => {
#                 sendPositionToStreamlit(null, null);
#             },
#             {
#                 enableHighAccuracy: true,
#                 timeout: 10000,
#                 maximumAge: 0
#             }
#         );
#         </script>
#         """,
#         height=0,
    # )
    # coords = st_javascript("""
    #     await new Promise((resolve) => {
    #         navigator.geolocation.getCurrentPosition(
    #             pos => resolve([pos.coords.latitude, pos.coords.longitude]),
    #             err => {
    #                 console.log("Geolocation failed:", err.message);
    #                 resolve(null);
    #             },
    #             {
    #                 enableHighAccuracy: true,
    #                 timeout: 10000,
    #                 maximumAge: 0
    #             }
    #         );
    #     });
    # """)
    # if "coords" not in st.session_state:
    #     st.session_state.coords = None
    # coords = st.experimental_get_query_params().get("coords")
    # if coords:
    #     lat, lon = coords
    #     st.success(f"📍 Position détectée via navigateur : {lat}, {lon}")
    #     return lat, lon

    # st.warning("🌐 Géolocalisation refusée ou échouée. Essai via IP...")
    lat, lon = get_fallback_location()
    print(lat)
    if lat and lon:
        st.info(f"📡 Position estimée par IP : {lat}, {lon}")
        return lat, lon

    # print(coords)
    if lat:
        # lat, lon = coords
        # print(coords)
        st.success(f"📌 Position détectée ! Latitude: {lat}, Longitude: {lon}")
    else:
        st.warning("🙈 Je n’ai pas pu te localiser… pas grave, on peut faire autrement !")


# Now lat & lon can be used to query GeoRisques, etc.
# Add this function to call the GeoRisques API using lat/lon

def get_georisques_nearby(lat, lon, rayon=1000, page=1, page_size=10):
    """
    Call the GeoRisques API with lat/lon coordinates to get nearby risks.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        rayon (int): Search radius in meters (default 1000)
        page (int): Page number (default 1)
        page_size (int): Results per page (default 10)

    Returns:
        dict: Risks data or error message
    """
    try:
        url = "https://www.georisques.gouv.fr/api/v1/gaspar/risques"
        params = {
            "latlon": f"{lon},{lat}",  # ⚠️ NOTE: lon,lat order!
            "rayon": rayon,
            "page": page,
            "page_size": page_size
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"GeoRisques API returned {response.status_code}: {response.text}"}

        return response.json()

    except Exception as e:
        return {"error": str(e)}


def format_georisques_summary(data: dict) -> str:
    """
    Format the GeoRisques API response into a human-readable summary.

    Args:
        data (dict): API response from /v1/gaspar/risques

    Returns:
        str: Markdown-formatted summary
    """
    if not data.get("data"):
        return "❌ Aucun risque identifié dans la zone."

    summary = "## 🌍 Risques environnementaux détectés\n\n"

    for commune in data["data"]:
        nom_commune = commune.get("libelle_commune", "Commune inconnue")
        code_insee = commune.get("code_insee", "")
        risques = commune.get("risques_detail", [])

        summary += f"### 📍 **{nom_commune}** *(INSEE: {code_insee})*\n"
        summary += "**Risques identifiés :**\n\n"

        for risque in risques:
            libelle = risque.get("libelle_risque_long", "Risque non précisé")
            summary += f"- 🔸 {libelle}\n"

        summary += "\n"

    return summary




def render_emergency_form():
    """
    Render the emergency situation form.
    
    Returns:
        Dictionary with form data
    """
    with st.form("emergency_form"):
        lat, lon = None, None

        st.title("📍 Trouvons où tu es… en douceur 🐾")

        st.markdown("Souhaites-tu que je détecte ta position automatiquement ?")

        use_geoloc = st.checkbox("Oui, géolocalise-moi ! 🌍")
        dont_use_geoloc = st.checkbox("Non, J'entre moi même une adresse ! 🌍")
        if use_geoloc:
            lat,lon=get_fallback_location()
            print(lat)
        dont_use_geoloc = st.checkbox("Non, J'entre moi même une adresse ! 🌍")
        if dont_use_geoloc:
            st.subheader("📝 Entre ton adresse manuellement")
            address = st.text_input("Où es-tu ?", placeholder="Ex : 15 rue Victor Hugo, Bordeaux")

            if address:
                def geocode_nominatim(query):
                    url = "https://nominatim.openstreetmap.org/search"
                    params = {"q": query, "format": "json", "limit": 1}
                    headers = {"User-Agent": "streamlit-crisis-buddy"}
                    r = requests.get(url, params=params, headers=headers)
                    if r.ok and r.json():
                        return float(r.json()[0]["lat"]), float(r.json()[0]["lon"])
                    return None, None

                lat, lon = geocode_nominatim(address)
                if lat and lon:
                    st.success(f"📍 Position trouvée ! Latitude: {lat}, Longitude: {lon}")
                else:
                    st.error("🧐 Adresse introuvable… vérifie l’orthographe peut-être ?")

        # lat, lon = None, None
        formatted=None

        if lat and lon:
            # st.subheader("🌋 Risques environnementaux autour de vous")
            risks_data = get_georisques_nearby(lat, lon)

            if "error" in risks_data:
                st.error(risks_data["error"])
            elif risks_data:
                formatted = format_georisques_summary(risks_data)
                # st.markdown(formatted)
            else:
                st.info("Aucun risque connu autour de cette position.") 
        # Situation description
        situation = st.text_area(
            "Describe the emergency situation",
            placeholder="Provide details about what happened...",
            help="Be specific about the situation to get the most relevant guidance"
        )
        
        # Emergency type
        emergency_types = [
            "Select emergency type",
            "Bleeding/Wounds",
            "Burns",
            "Cardiac Emergency",
            "Choking",
            "Fractures/Sprains",
            "Head Injury",
            "Heat/Cold Emergency",
            "Poisoning",
            "Seizure",
            "Shock",
            "Other Medical Emergency",
            "Natural Disaster",
            "Fire Emergency",
            "Water Emergency"
        ]
        
        emergency_type = st.selectbox(
            "Type of Emergency",
            options=emergency_types
        )
        
        # Additional details
        col1, col2 = st.columns(2)
        
        with col1:
            severity = st.select_slider(
                "Severity",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
            
        with col2:
            age_group = st.selectbox(
                "Age Group",
                options=["Infant (0-1)", "Child (1-12)", "Teen (13-17)", "Adult (18-65)", "Elderly (65+)"],
                index=3
            )
        
        # Submit button
        submit_button = st.form_submit_button("Get Emergency Guidance", type="primary")
        
        if submit_button:
            if emergency_type == "Select emergency type":
                st.error("Please select an emergency type")
                return None
            
            if not situation or len(situation.strip()) < 10:
                st.error("Please provide more details about the situation (description too short)")
                return None
            
            return {
                "geoloc":formatted,
                "situation": situation,
                "emergency_type": emergency_type,
                "severity": severity.lower(),
                "age_group": age_group
            }
        
        return None