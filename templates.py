# Custom HTML/CSS component templates for the Music Dashboard UI

def get_intervention_card(track_name, bpm):
    return f"""
    <div class='spotify-card track-active'>
        <h4 style='color: #ff4b4b; margin-top:0;'>⚠️ Smart Intervention Recommended</h4>
        <p>Your biometric markers indicate high sympathetic nervous system activation. The currently active track <b>({track_name})</b> has an intense tempo of <b>{bpm} BPM</b>, which might compound anxiety.</p>
        <p style='color: #1db954;'><b>💡 Prescriptive Suggestion:</b> Click on <b>'Weightless - Marconi Union'</b> or <b>'Clair de Lune'</b> in the library sidebar to trigger an acoustic down-tempo mitigation trajectory.</p>
    </div>
    """

def get_safe_card():
    return """
    <div class='spotify-card track-safe'>
        <h4 style='color: #00cdff; margin-top:0;'>ℹ️ Optimization Track Active</h4>
        <p>Physiological stress detected, but your manual transition to a low-tempo acoustic baseline is actively assisting down-regulation. Maintain listening posture.</p>
    </div>
    """

def get_homeostasis_card():
    return """
    <div class='spotify-card'>
        <h4 style='color: #1db954; margin-top:0;'>✅ Physiological Balance Maintained</h4>
        <p>Your biometric indicators are optimal. No adaptive musical intervention or context switching is required at this time.</p>
    </div>
    """tem
