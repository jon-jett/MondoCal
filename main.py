from mondocal import make_calendar, PDF


calendar_settings = {
    "Title": "SPRING 2024",
    "Title Color": "#000000",
    "Start Date": "1/1/2024",
    "End Date": "5/31/2024",
    "M1": "#24D6E3",  #
    "M2": "#FFA500",  # Orange
    "M3": "#FFD700",  # Yellow (darker for readability)
    "M4": "#008000",  # Green
    "M5": "#0000FF",  # Blue
    "M6": "#8A2BE2",  # Violet
    "Narrow Percent": 1.5,
    "Narrow Pixels": None,
    "Thick Percent": 4.5,
    "Thick Pixels": None,
    "Date Margin Multiplier": 1.5,
    "Month Margin Multiplier": 1.5,
    "Date Margin Pixels": None,
    "Margin": 1,
    "Title Height": 1.5 ,
    "Top Title Proportion": .8,
    "Top Margin Pixels": None,
    "Margin Pixels": None,
    "Date Font Size": 200,
    "Month Font Size": 200,
    "Start Day": "Monday",
    "Paper Width": 22,  # Renamed from Total Width
    "Paper Height": 42,  # Renamed from Total Height
    "Month Width": 0.5,
    "Month Width Pixels": None,
    "font_path": "Poppins/Poppins-Regular.ttf",
    "font_path_bold": "Poppins/Poppins-Bold.ttf",
    "font_path_italic": "Poppins/Poppins-Italic.ttf",
    "font_path_title": "Poppins/Poppins-Medium.ttf",
    "PPI": 300,
    "weekend_shader": "#f4f4f4",
    "weekend_shader_color": "black",
    "Total Rows": None,
    "January Color": "#D3D3D3",
    "February Color": "#D3D3D3",
    "March Color": "#D3D3D3",
    "April Color": "#D3D3D3",
    "May Color": "#D3D3D3",
    "June Color": "#D3D3D3",
    "July Color": "#D3D3D3",
    "August Color": "#D3D3D3",
    "September Color": "#D3D3D3",
    "October Color": "#D3D3D3",
    "November Color": "#D3D3D3",
    "December Color": "#D3D3D3",
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

# Save the calendar image
calendar_image.save("calendar.png")





calendar_pdf.output("calendar.pdf")