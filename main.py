from mondocal import make_calendar


calendar_settings = {
    "Title": "SPRING 2025",
    "Title Color": "#000000",
    "Start Date": "1/1/2025",
    "End Date": "4/30/2025",
    "Narrow Percent": 1.5,
    "Thick Percent": 4.5,
    "Date Margin Multiplier": 1.5,
    "Month Margin Multiplier": 1.5,
    "Margin": 1,
    "Title Height": 1.5,
    "Top Title Proportion": 0.8,
    "Date Font Size": 160,
    "Month Font Size": 200,
    "Start Day": "Sunday",
    "Paper Width": 26,  # Renamed from Total Width
    "Paper Height": 40,  # Renamed from Total Height
    "Month Width": 0.5,
    "Font Path Day": "Poppins/Poppins-Regular.ttf",
    "Font Path Month": "Poppins/Poppins-Bold.ttf",
    "Font Path Title": "Poppins/Poppins-Medium.ttf",
    "PPI": 300,
    "weekend_shader": "#e5e5e5",
    "weekend_shader_color": "black",
    "Uniform Narrow Lines": True,
    "Narrow Lines Color": "#777777",
    "DOTW Color": "#000000",
    "Center Month": True,
}


rainbow_violet_sequence = {
    "M1": "#FF0000",  # Red
    "M2": "#FF9800",  # Orange
    "M6": "#8A2BE2",  # Violet
    "M3": "#008000",  # Green
    "M4": "#0000FF",  # Blue
    "M5": "#4B0082",  # Indigo
}

rainbow_light_blue = {
    "M1": "#FF0000",  # Red
    "M2": "#FFA500",  # Orange
    "M3": "#ADD8E6",  # Light Blue
    "M4": "#008000",  # Green
    "M5": "#0000FF",  # Blue
    "M6": "#8A2BE2",  # Violet
}
rainbow_green_sequence = {
    "M1": "#FF0000",  # Red
    "M2": "#FFA500",  # Orange
    "M3": "#008000",  # Green
    "M4": "#0000FF",  # Blue
    "M5": "#4B0082",  # Indigo
    "M6": "#8A2BE2",  # Violet
}

rainbow_colors = {
    "M1": "#FF0000",  # Red
    "M2": "#FFA500",  # Orange
    "M3": "#FFD700",  # Yellow (darker for readability)
    "M4": "#008000",  # Green
    "M5": "#0000FF",  # Blue
    "M6": "#8A2BE2",  # Violet
}

sea_colors = {
    "M1": "#0B3D91",  # Deep Blue
    "M2": "#197278",  # Teal
    "M3": "#006D5B",  # Turquoise
    "M4": "#48A9A6",  # Aquamarine
    "M5": "#1B4F72",  # Navy Blue
    "M6": "#3B9B74",  # Sea Green
}
autumn_colors = {
    "M1": "#FF6347",  # Tomato
    "M2": "#FFA07A",  # Light Salmon
    "M3": "#FF7F50",  # Coral
    "M4": "#CD853F",  # Peru
    "M5": "#A0522D",  # Sienna
    "M6": "#8B0000",  # Dark Red
}

sky_colors = {
    "M1": "#87CEFA",  # Light Sky Blue
    "M2": "#4682B4",  # Steel Blue
    "M3": "#6495ED",  # Cornflower Blue
    "M4": "#7B68EE",  # Medium Slate Blue
    "M5": "#6A5ACD",  # Slate Blue
    "M6": "#4169E1",  # Royal Blue
}

earth_colors = {
    "M1": "#D2B48C",  # Tan
    "M2": "#DEB887",  # Burlywood
    "M3": "#DAA520",  # Goldenrod
    "M4": "#B8860B",  # Dark Goldenrod
    "M5": "#CD853F",  # Peru
    "M6": "#BC8F8F",  # Rosy Brown
}
sunset_colors = {
    "M1": "#DB7093",  # Pale Violet Red
    "M2": "#FF69B4",  # Hot Pink
    "M3": "#FFB6C1",  # Light Pink
    "M4": "#DDA0DD",  # Plum
    "M5": "#DA70D6",  # Orchid
    "M6": "#BA55D3",  # Medium Orchid
}
monochrome_colors = {
    "M1": "#2F4F4F",  # Dark Slate Gray
    "M2": "#696969",  # Dim Gray
    "M3": "#A9A9A9",  # Dark Gray
    "M4": "#C0C0C0",  # Silver
    "M5": "#D3D3D3",  # Light Gray
    "M6": "#808080",  # Gray
}


calendar_settings.update(rainbow_violet_sequence)


calendar_image, calendar_pdf = make_calendar(calendar_settings)


calendar_pdf.output("calendar.pdf")
