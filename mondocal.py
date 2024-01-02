from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import math
from icecream import ic
import os

calendar_settings = {
    "Start Date": "1/1/2024",
    "End Date": "1/20/2024",
    "M1": "#64F2F5",
    "M2": "#6f005a",
    "M3": "#ffed3b",
    "M4": "#64F5C6",
    "M5": "#5D62F5",
    "M6": "#64F2F5",
    "Narrow Percent": 2,
    "Narrow Pixels": None,
    "Thick Percent": 6,
    "Thick Pixels": None,
    "Date Margin Multiplier": 1.1,
    "Date Margin Pixels": None,
    "Margin": 1,
    "Margin Pixels": None,
    "Date Font": 200,
    "Month Font": 140,
    "Start Day": "Monday",
    "Paper Width": 22,  # Renamed from Total Width
    "Paper Height": 10,  # Renamed from Total Height
    "Month Width": 1.25,
    "Month Width Pixels": None,
    "font_path": "Poppins/Poppins-Regular.ttf",
    "font_path_bold": "Poppins/Poppins-Bold.ttf",
    "font_path_italic": "Poppins/Poppins-Italic.ttf",
    "PPI": 300,
    "weekend_shader": 0.1,
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
}


class Day:
    def __init__(self, date_str, calendar_settings):
        # Convert date string to datetime object for easy manipulation
        self.date = datetime.strptime(date_str, "%m/%d/%Y")

        # Set the color based on the month
        self.color = calendar_settings[f"{self.date.strftime('%B')} Color"]

        # These properties depend on your specific layout logic
        self.row = self.calculate_row()
        self.column = self.date.weekday()

        # Text for the day, usually the day number
        self.text = str(
            self.date.day
        )  # Converts the day part to an integer, then to a string

        # Calculate the position of the day in the grid
        start_x = int(calendar_settings["Margin Pixels"]) + int(
            calendar_settings["Month Width Pixels"]
        )
        start_y = 2 * calendar_settings["Margin Pixels"]
        #ic(start_x, start_y)
        day_width = calendar_settings["Day Width"]
        day_height = calendar_settings["Day Height"]

        # Calculate top-left corner
        self.top_left = (
            start_x + (self.column - 1) * day_width,
            start_y + (self.row - 1) * day_height,
        )

        # Calculate top-right corner
        self.top_right = (self.top_left[0] + day_width, self.top_left[1])

        # Calculate bottom-left corner
        self.bottom_left = (self.top_left[0], self.top_left[1] + day_height)

        # Calculate bottom-right corner
        self.bottom_right = (
            self.top_left[0] + day_width,
            self.top_left[1] + day_height,
        )

        # Create an image for this day
        self.image = None

    def calculate_row(self):
        # Find the first day of the first week in the calendar
        start_date = datetime.strptime(calendar_settings["Start Date"], "%m/%d/%Y")
        first_day_of_calendar = start_date - timedelta(days=start_date.weekday())

        # Calculate the difference in days from the first day of the calendar
        days_from_first_day = (self.date - first_day_of_calendar).days

        # Calculate the row (add 1 because we're starting from 1, not 0)
        row = math.ceil((days_from_first_day + 1) / 7)
        return row

    def create_day_image(self):
        # Define the image dimensions
        width, height = int(calendar_settings["Day Width"]), int(
            calendar_settings["Day Height"]
        )

        # Create a new image with a white background
        self.image = Image.new("RGB", (width, height), "white")

        # Create a draw object
        draw = ImageDraw.Draw(self.image)

        # Load the font
        try:
            font = ImageFont.truetype(
                calendar_settings["font_path"], size=calendar_settings["Date Font"]
            )
        except IOError:
            font = ImageFont.load_default()

        # Get the bounding box of the text
        text_bbox = font.getbbox(self.text)

        # Calculate the position for the date text
        text_x = (
            width - text_bbox[2] - calendar_settings["Date Margin Pixels"]
        )  # Adjust the margin as needed
        text_y = (
            calendar_settings["Date Margin Pixels"] - text_bbox[1]
        )  # Adjust vertical position

        # Draw the date text on the image
        draw.text((text_x, text_y), self.text, fill=self.color, font=font)

        # Draw the border
        border_width = int(calendar_settings["Narrow Pixels"])
        draw.rectangle([0, 0, width, height], outline=self.color, width=border_width)

        return self.image


# Helper function to round down to the nearest even integer
def round_down_to_even(number):
    rounded_number = math.floor(number)
    return rounded_number if rounded_number % 2 == 0 else rounded_number - 1


##### Calculate Calendar Graphical Setup
# Convert inches to pixels
calendar_settings["Paper Pixel Width"] = (
    calendar_settings["Paper Width"] * calendar_settings["PPI"]
)
calendar_settings["Paper Pixel Height"] = (
    calendar_settings["Paper Height"] * calendar_settings["PPI"]
)
calendar_settings["Month Width Pixels"] = (
    calendar_settings["Month Width"] * calendar_settings["PPI"]
)

# Default margin if not specified
calendar_settings["Margin Pixels"] = (
    calendar_settings["Margin"] * calendar_settings["PPI"]
)

# Calculate print width and height
calendar_settings["Print Width"] = (
    calendar_settings["Paper Pixel Width"]
    - (2 * calendar_settings["Margin Pixels"])
    - calendar_settings["Month Width Pixels"]
)
calendar_settings["Print Height"] = (
    calendar_settings["Paper Pixel Height"] - 3 * calendar_settings["Margin Pixels"]
)
# ic(calendar_settings["Paper Pixel Width"], calendar_settings["Paper Pixel Height"], calendar_settings["Print Width"], calendar_settings["Print Height"])


# Calculate day width and round down to the nearest even integer
calendar_settings["Day Width"] = round_down_to_even(
    (calendar_settings["Print Width"] - calendar_settings["Month Width"]) / 7
)

# Calculate the total number of weeks in the date range
calendar_settings["start_date"] = datetime.strptime(
    calendar_settings["Start Date"], "%m/%d/%Y"
)
calendar_settings["end_date"] = datetime.strptime(
    calendar_settings["End Date"], "%m/%d/%Y"
)
calendar_settings["total_days"] = (
    calendar_settings["end_date"] - calendar_settings["start_date"]
).days + 1
calendar_settings["total_weeks"] = math.ceil(calendar_settings["total_days"] / 7)

# Calculate day height and round down to the nearest even integer
calendar_settings["Day Height"] = round_down_to_even(
    (calendar_settings["Print Height"] - calendar_settings["Month Width"])
    / calendar_settings["total_weeks"]
)


# Calculate the narrow,thick and date margin pixel values
calendar_settings["Narrow Pixels"] = (
    calendar_settings["Narrow Percent"] / 100 * calendar_settings["Day Width"]
)
calendar_settings["Thick Pixels"] = (
    calendar_settings["Thick Percent"] / 100 * calendar_settings["Day Width"]
)
calendar_settings["Date Margin Pixels"] = (
    calendar_settings["Thick Pixels"] * calendar_settings["Date Margin Multiplier"]
)


# Function to iterate through each day in the range and create Day objects
def create_calendar_days():
    days_with_images = {}
    current_date = calendar_settings["start_date"]
    while current_date <= calendar_settings["end_date"]:
        day_obj = Day(current_date.strftime("%m/%d/%Y"), calendar_settings)
        day_image = day_obj.create_day_image()
        day_obj.image = day_image
        days_with_images[current_date.strftime("%m-%d-%Y")] = day_obj
        current_date += timedelta(days=1)

    return days_with_images


def save_calendar_images(days_with_images):
    for date_str, day in days_with_images.items():
        image = day.image
        image.save(os.path.join("temp", f"{date_str}.jpg"))


def find_max_font_size(font_path, text, max_width, max_height):
    font_size = 2  # Starting font size
    while True:
        # Create a font object with the current font size
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print("Font file not found. Please check the font path.")
            return None

        # Get the bounding box of the text
        text_width, text_height = font.getbbox(text)[2:]

        # Check if the text exceeds the maximum dimensions
        if text_width > max_width or text_height > max_height:
            return (
                font_size - 1
            )  # Return the previous size that fit within the dimensions

        # Increment the font size for the next iteration
        font_size += 1


def create_month_list(start_date_str, end_date_str):
    # Convert start and end dates from string to datetime objects
    start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
    end_date = datetime.strptime(end_date_str, "%m/%d/%Y")

    # Check if the first month is a full month
    if not month_has_full_week(start_date, get_first_last_day_of_month(start_date)[1]):
        start_date = start_date.replace(day=1, month=start_date.month + 1)

    # Check if the last month is a full month
    if not month_has_full_week(get_first_last_day_of_month(end_date)[0], end_date):
        end_date = end_date.replace(day=1) - timedelta(days=1)

    # Create a list to hold the months
    months = []

    # Start iterating from the actual start date
    current_date = start_date

    while current_date <= end_date:
        current_month = current_date.month
        if current_month not in months:
            months.append(current_month)

        # Move to the next day
        current_date = current_date + timedelta(days=1)

    month_names = [datetime(1, month_num, 1).strftime("%B") for month_num in months]

    return month_names


def month_has_full_week(start_of_month, end_of_month):
    current_date = start_of_month

    # Find the first Monday in the month
    while current_date <= end_of_month:
        if current_date.weekday() == 0:  # 0 represents Monday
            break  # Found the first Monday
        current_date += timedelta(days=1)

    # If we didn't find a Monday before the end of the month, return False
    if current_date > end_of_month:
        return False

    # Continue from the found Monday to find a Sunday or reach the end of the month
    while current_date <= end_of_month:
        if current_date.weekday() == 6:  # 6 represents Sunday
            return True  # Found a full week from Monday to Sunday
        current_date += timedelta(days=1)

    # If we reached the end of the month without finding a full week, return False
    return False


def get_first_last_day_of_month(date):
    # First day of the month is always the 1st
    first_day = date.replace(day=1)

    # Last day of the month can be found by moving to the first day of the next month and subtracting one day
    if date.month == 12:
        # If the current month is December, the next month is January of the next year
        next_month = date.replace(year=date.year + 1, month=1, day=1)
    else:
        # For other months, just increment the month
        next_month = date.replace(month=date.month + 1, day=1)

    last_day = next_month - timedelta(days=1)

    return first_day, last_day


def assign_month_colors(months, calendar_settings):
    # Create an iterator for month color settings
    month_color_keys = iter(["M1", "M2", "M3", "M4", "M5", "M6"])

    for month in months:
        try:
            # Get the next month color
            month_color_key = next(month_color_keys)
        except StopIteration:
            # Restart the iterator if there are more months than color keys
            month_color_keys = iter(["M1", "M2", "M3", "M4", "M5", "M6"])
            month_color_key = next(month_color_keys)

        # Update the calendar settings with the specific color for that month
        calendar_settings[f"{month} Color"] = calendar_settings[month_color_key]


def create_calendar_with_days(days_with_images, calendar_settings):
    # Create a new image for the entire calendar
    paper_width_pixels = calendar_settings["Paper Pixel Width"]
    paper_height_pixels = calendar_settings["Paper Pixel Height"]
    calendar_image = Image.new(
        "RGB", (paper_width_pixels, paper_height_pixels), "white"
    )

    for day_image in days_with_images.values():
        # Get the position to paste the day image
        top_left_x, top_left_y = day_image.top_left

        # Paste the day image onto the calendar image
        calendar_image.paste(
            day_image.image,
            (
                int(
                    top_left_x
                    + calendar_settings["Month Width Pixels"]
                    + calendar_settings["Margin Pixels"]
                ),
                int(top_left_y),
            ),
        )

    # return the calendar image

    return calendar_image


def add_days_of_week_to_calendar(calendar_image, calendar_settings):
    days_of_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    # Use the same start_x and start_y as in the Day class
    start_x = int(calendar_settings["Margin Pixels"]) + int(calendar_settings["Month Width Pixels"])
    start_y = 2 * calendar_settings["Margin Pixels"]  # Adjust this value if needed
    ic("now", start_x, start_y)
    day_width = calendar_settings["Day Width"]

    draw = ImageDraw.Draw(calendar_image)

    # Add a red vertical line at the start location for testing
    line_end_y = calendar_settings["Paper Pixel Height"] - calendar_settings["Margin Pixels"]
    draw.line([(start_x, start_y), (start_x, line_end_y)], fill="red", width=1)

    # Calculate maximum font size that fits "WEDNESDAY" within the given dimensions
    max_font_width = int(day_width * 0.80)  # 80% of day_width
    max_font_height = 10000  # Arbitrarily large

    # Find the maximum font size for "WEDNESDAY"
    max_font_size = find_max_font_size(calendar_settings["font_path"], "WEDNESDAY", max_font_width, max_font_height)
    font = ImageFont.truetype(calendar_settings["font_path"], size=max_font_size)

    # Get the bounding box of "WEDNESDAY" for vertical alignment calculation
    wednesday_bbox = font.getbbox("WEDNESDAY")
    wednesday_height = wednesday_bbox[3] - wednesday_bbox[1]

    for i, day in enumerate(days_of_week):
        center_x = start_x + (i * day_width) + (day_width / 2)

        # Use getbbox to get the bounding box of the text for each day
        text_bbox = font.getbbox(day)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        ic(text_width, text_height)

        # Adjust the text position to be centered and higher up
        text_x = center_x - (text_width / 2)
        text_y = start_y - (wednesday_height) - text_height

        draw.text((text_x, text_y), day, fill="black", font=font)

    return calendar_image




# Get list of months in the date range that get colors
month_list = create_month_list(
    calendar_settings["Start Date"], calendar_settings["End Date"]
)

# Assign colors to the months
assign_month_colors(month_list, calendar_settings)

# Generate the images
days_with_images = create_calendar_days()

# Save the images to a temp folder
# save_calendar_images(days_with_images)


# Assuming days_with_images is already populated with Day objects
calendar_with_days = create_calendar_with_days(days_with_images, calendar_settings)

calendar_with_weekdays = add_days_of_week_to_calendar(
    calendar_with_days, calendar_settings
)



calendar_with_weekdays.save("calendar1.jpg")

for day in days_with_images.values():
    ic(day.date, day.top_left, day.top_right, day.bottom_left, day.bottom_right)
