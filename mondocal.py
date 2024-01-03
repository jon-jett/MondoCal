from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import math
from icecream import ic
import os
from fpdf import FPDF


class Day:
    def __init__(self, date_str, calendar_settings):
        # Convert date string to datetime object for easy manipulation
        self.date = datetime.strptime(date_str, "%m/%d/%Y")

        # Set the color based on the month
        self.color = calendar_settings[f"{self.date.strftime('%B')} Color"]

        # These properties depend on your specific layout logic
        self.row = self.calculate_row(calendar_settings)
        self.column = self.date.weekday() + 1  # Monday is 1, Sunday is 7

        # Text for the day, usually the day number
        self.text = str(
            self.date.day
        )  # Converts the day part to an integer, then to a string

        # Calculate the position of the day in the grid
        start_x = int(calendar_settings["Margin Pixels"]) + int(
            calendar_settings["Month Width Pixels"]
        )
        start_y = (
            calendar_settings["Margin Pixels"] + calendar_settings["Top Margin Pixels"]
        )

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

    def calculate_row(self, calendar_settings):
        # Find the first day of the first week in the calendar
        start_date = datetime.strptime(calendar_settings["Start Date"], "%m/%d/%Y")
        first_day_of_calendar = start_date - timedelta(days=start_date.weekday())

        # Calculate the difference in days from the first day of the calendar
        days_from_first_day = (self.date - first_day_of_calendar).days

        # Calculate the row (add 1 because we're starting from 1, not 0)
        row = math.ceil((days_from_first_day + 1) / 7)
        return row

    def create_day_image(self, calendar_settings):
        # Define the image dimensions
        width, height = int(calendar_settings["Day Width"]), int(
            calendar_settings["Day Height"]
        )

        # Create a new image with a white background for days M-F and a shaded background for weekends
        if self.date.weekday() < 5:
            self.image = Image.new("RGB", (width, height), "white")
        else:
            self.image = Image.new(
                "RGB", (width, height), calendar_settings["weekend_shader"]
            )

        # Create a draw object
        draw = ImageDraw.Draw(self.image)

        # Load the font
        try:
            font = ImageFont.truetype(
                calendar_settings["Font Path Day"],
                size=calendar_settings["Date Font Size"],
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
        if calendar_settings["Uniform Narrow Lines"]:
            draw.rectangle(
                [0, 0, width, height],
                outline=calendar_settings["Narrow Lines Color"],
                width=border_width,
            )
        else:
            draw.rectangle(
                [0, 0, width, height], outline=self.color, width=border_width
            )

        return self.image


class PDF(FPDF):
    def __init__(
        self,
        dpi,
        pixel_width,
        pixel_height,
        doc_width_inch,
        doc_height_inch,
        margin_inch,
        image_path,
    ):
        super().__init__(
            orientation="P", unit="in", format=(doc_width_inch, doc_height_inch)
        )
        self.dpi = dpi
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.img_width_inch = pixel_width / dpi
        self.img_height_inch = pixel_height / dpi
        self.margin_inch = margin_inch
        self.image_path = image_path
        self.add_image_page()

    def add_image_page(self):
        self.add_page()
        # Load the PNG image
        img = Image.open(self.image_path)
        # Calculate the width and height in inches
        img_width_inch = img.width / self.dpi
        img_height_inch = img.height / self.dpi
        # Calculate the position to center the image
        x = (self.w - img_width_inch) / 2
        y = (self.h - img_height_inch) / 2
        # Add the image to the PDF
        self.image(self.image_path, x=x, y=y, w=img_width_inch, h=img_height_inch)


# Helper function to round down to the nearest even integer
def round_down_to_even(number):
    rounded_number = math.floor(number)
    return rounded_number if rounded_number % 2 == 0 else rounded_number - 1


##### Calculate Calendar Graphical Setup
def initialize_calendar_settings(calendar_settings):
    noneditable_settings = {
        "Month Width Pixels": None,
        "Date Margin Pixels": None,
        "Total Rows": None,
        "Top Margin Pixels": None,
        "Margin Pixels": None,
        "Thick Pixels": None,
        "Narrow Pixels": None,
        "January Color": calendar_settings["Narrow Lines Color"],
        "February Color": calendar_settings["Narrow Lines Color"],
        "March Color": calendar_settings["Narrow Lines Color"],
        "April Color": calendar_settings["Narrow Lines Color"],
        "May Color": calendar_settings["Narrow Lines Color"],
        "June Color": calendar_settings["Narrow Lines Color"],
        "July Color": calendar_settings["Narrow Lines Color"],
        "August Color": calendar_settings["Narrow Lines Color"],
        "September Color": calendar_settings["Narrow Lines Color"],
        "October Color": calendar_settings["Narrow Lines Color"],
        "November Color": calendar_settings["Narrow Lines Color"],
        "December Color": calendar_settings["Narrow Lines Color"],
    }
    calendar_settings.update(noneditable_settings)
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
    calendar_settings["Top Margin Pixels"] = int(
        (calendar_settings["Title Height"] * calendar_settings["PPI"])
    )
    calendar_settings["Margin Pixels"] = (
        calendar_settings["Margin"] * calendar_settings["PPI"]
    )

    # Calculate print width and height
    calendar_settings["Print Width"] = calendar_settings["Paper Pixel Width"] - (
        2 * calendar_settings["Margin Pixels"]
    )
    calendar_settings["Print Height"] = (
        calendar_settings["Paper Pixel Height"]
        - 2 * calendar_settings["Margin Pixels"]
        - calendar_settings["Top Margin Pixels"]
    )

    # Calculate day width and round down to the nearest even integer
    calendar_settings["Day Width"] = round_down_to_even(
        (calendar_settings["Print Width"] - calendar_settings["Month Width Pixels"]) / 7
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
        calendar_settings["Print Height"] / calendar_settings["total_weeks"]
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
    return calendar_settings


# Function to iterate through each day in the range and create Day objects
def create_day_objects(calendar_settings):
    days_with_images = {}
    current_date = calendar_settings["start_date"]
    while current_date <= calendar_settings["end_date"]:
        day_obj = Day(current_date.strftime("%m/%d/%Y"), calendar_settings)
        day_image = day_obj.create_day_image(calendar_settings)
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
                int(top_left_x),
                int(top_left_y),
            ),
        )

    # return the calendar image

    return calendar_image


def add_days_of_week_to_calendar(calendar_image, calendar_settings):
    days_of_week = [
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY",
    ]

    # Use the same start_x and start_y as in the Day class
    start_x = int(calendar_settings["Margin Pixels"]) + int(
        calendar_settings["Month Width Pixels"]
    )
    start_y = (
        calendar_settings["Margin Pixels"] + calendar_settings["Top Margin Pixels"]
    )  # Adjust this value if needed

    day_width = calendar_settings["Day Width"]

    draw = ImageDraw.Draw(calendar_image)

    # Add a red vertical line at the start location for tralfamadorian testing
    # line_end_y = calendar_settings["Paper Pixel Height"] - calendar_settings["Margin Pixels"]
    # draw.line([(start_x, start_y), (start_x, line_end_y)], fill="red", width=1)

    # Calculate maximum font size that fits "WEDNESDAY" within the given dimensions
    max_font_width = int(day_width * 0.80)  # 80% of day_width
    max_font_height = 10000  # Arbitrarily large

    # Find the maximum font size for "WEDNESDAY"
    max_font_size = find_max_font_size(
        calendar_settings["Font Path Day"], "WEDNESDAY", max_font_width, max_font_height
    )
    font = ImageFont.truetype(calendar_settings["Font Path Day"], size=max_font_size)

    # Get the bounding box of "WEDNESDAY" for vertical alignment calculation
    wednesday_bbox = font.getbbox("WEDNESDAY")
    wednesday_height = wednesday_bbox[3] - wednesday_bbox[1]

    for i, day in enumerate(days_of_week):
        center_x = start_x + (i * day_width) + (day_width / 2)

        # Use getbbox to get the bounding box of the text for each day
        text_bbox = font.getbbox(day)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Adjust the text position to be centered and higher up
        text_x = center_x - (text_width / 2)
        text_y = start_y - (wednesday_height) - text_height

        draw.text(
            (text_x, text_y), day, fill=calendar_settings["DOTW Color"], font=font
        )

    return calendar_image


def draw_thick_lines(calendar_image, calendar_settings, days_with_images, month_list):
    for index, each in enumerate(month_list):
        is_last_month = (
            index == len(month_list) - 1
        )  # Check if this is the last month in the list
        if is_last_month:
            last_adj = 0
        else:
            last_adj = 1
        month_color = calendar_settings[f"{each} Color"]
        days_for_thick_lines = [
            day for day in days_with_images.values() if day.date.strftime("%B") == each
        ]
        first_week = days_for_thick_lines[:7]
        last_week = days_for_thick_lines[-7:]
        first_day = days_for_thick_lines[0]
        last_day = days_for_thick_lines[-1]
        mondays = [day for day in days_for_thick_lines if day.date.weekday() == 0]
        sundays = [day for day in days_for_thick_lines if day.date.weekday() == 6]
        draw = ImageDraw.Draw(calendar_image)
        adj = int(calendar_settings["Thick Pixels"] / 2)

        # Draw lines at the bottom first, adjusted to make them thinner once they're overwritten by the top lines
        for day in last_week:
            # Adjusting the Y-coordinate of both points by subtracting 'adj'
            start_point = (day.bottom_left[0], day.bottom_left[1] - adj * 2 * last_adj)
            end_point = (day.bottom_right[0], day.bottom_right[1] - adj * 2 * last_adj)

            draw.line(
                [start_point, end_point],
                fill=month_color,
                width=int(calendar_settings["Thick Pixels"]),
            )

        # Draw lines at the right side of the last day, adjusting the top, except if the last day is a sunday, skip it
        if last_day.date.weekday() != 6:
            start_point = (
                last_day.bottom_right[0] - adj * last_adj,
                last_day.bottom_right[1] + adj,
            )
            end_point = (
                last_day.top_right[0] - adj * last_adj,
                last_day.top_right[1] - adj - 2 * adj * last_adj,
            )
            draw.line(
                [start_point, end_point],
                fill=month_color,
                width=int(calendar_settings["Thick Pixels"]),
            )

        # Draw lines at the left side of the first day
        start_point = (
            first_day.bottom_left[0] + adj,
            first_day.bottom_left[1] + adj * 1,
        )
        end_point = (first_day.top_left[0] + adj, first_day.top_left[1] - adj * 0)
        draw.line(
            [start_point, end_point],
            fill=month_color,
            width=int(calendar_settings["Thick Pixels"]),
        )

        # Draw lines at the top last, so we see the full width that overwrites the bottom ones
        for day in first_week:
            draw.line(
                [
                    day.top_left,
                    day.top_right,
                ],
                fill=month_color,
                width=int(calendar_settings["Thick Pixels"]),
            )

        # Draw lines at the left side of the month
        for day in mondays:
            start_point = (day.bottom_left[0] + adj, day.bottom_left[1] + adj * 1)
            end_point = (day.top_left[0] + adj, day.top_left[1] - adj * 0)
            draw.line(
                [start_point, end_point],
                fill=month_color,
                width=int(calendar_settings["Thick Pixels"]),
            )

        # Draw lines at the right side of the month
        for day in sundays:
            start_point = (day.bottom_right[0], day.bottom_right[1] + adj)
            end_point = (day.top_right[0], day.top_right[1] - adj * 1)
            draw.line(
                [start_point, end_point],
                fill=month_color,
                width=int(calendar_settings["Thick Pixels"]),
            )

    return calendar_image


# function to add month names to the calendar
# accepts calendar_image, calendar_settings, days_with_images, month_list as input
# for each month in month_list, generates a new image with the month name in the correct color, rotates it 90 CCW, and pastes it onto the calendar image in the correct location
# the correct location for each month is to the left of the first monday of that month, with the top of the month name aligned with the top of the first monday
# or if "Center Months" is True, the month name is centered between the top of the first monday and the bottom of the last monday and to the left
# returns the calendar image with the month names added
def add_months_to_calendar(
    calendar_image, calendar_settings, days_with_images, month_list
):
    font_size = calendar_settings["Month Font Size"]
    font = ImageFont.truetype(calendar_settings["Font Path Month"], size=font_size)

    for index, each in enumerate(month_list):
        month_color = calendar_settings[f"{each} Color"]
        month_name = each.upper()
        # find the first monday of the month
        days_for_month_labels = [
            day for day in days_with_images.values() if day.date.strftime("%B") == each
        ]
        mondays = [day for day in days_for_month_labels if day.date.weekday() == 0]
        # find coordinates for the top left corner of the first monday of the month
        first_monday = mondays[0]
        last_monday = mondays[-1]
        start_x, start_y = first_monday.top_left
        # calculate the bounding box of the month name, adding characters j and y to make sure the bounding box is large enough JY
        month_name_bbox = font.getbbox(each.upper())
        month_name_width = month_name_bbox[2] - month_name_bbox[0]
        month_name_height = month_name_bbox[3] - month_name_bbox[1]
        # check if the month_name_width is greater than height of the mondays in the month and replace it with an abbreviation if it is
        if month_name_width > (calendar_settings["Day Height"] * len(mondays)):
            month_name = each[:3].upper()
        # create an image for the month name using month color, month name, and font size, and calculated dimensions
        month_name_image = Image.new(
            "RGBA", (month_name_width, month_name_height), (0, 0, 0, 0)
        )
        draw = ImageDraw.Draw(month_name_image)
        draw.text((0, month_name_height // -2), month_name, fill=month_color, font=font)
        # rotate the image 90 CCW
        month_name_image = month_name_image.rotate(90, expand=True)
        # If "Center Months" is False, top justify the names of the months and paste the image onto the calendar image
        if not calendar_settings["Center Month"]:
            calendar_image.paste(
                month_name_image,
                (
                    int(
                        start_x
                        - month_name_height
                        * calendar_settings["Month Margin Multiplier"]
                    ),
                    start_y,
                ),
                month_name_image,
            )
        # If "Center Months" is True, center the names of the months
        # to do this we need to find the top of the first monday and the bottom of the last monday
        # then find the center of the space between them
        # then find the center of the month name
        else:
            # find the top of the first monday
            first_monday_top = first_monday.top_left[1]
            # find the bottom of the last monday
            last_monday_bottom = last_monday.bottom_left[1]
            # find the center of the space between them
            space_between = last_monday_bottom - first_monday_top
            space_between_center = space_between // 2
            # find the center of the month name
            month_name_center = month_name_height // 2
            # find the top of the month name
            month_name_top = space_between_center - month_name_width // 2
            # paste the image onto the calendar image
            calendar_image.paste(
                month_name_image,
                (
                    int(
                        start_x
                        - month_name_height
                        * calendar_settings["Month Margin Multiplier"]
                    ),
                    int(
                        start_y + month_name_top,
                    ),
                ),
                month_name_image,
            )

    return calendar_image


def make_calendar(calendar_settings):
    calendar_settings = initialize_calendar_settings(calendar_settings)
    # Get list of months in the date range that get colors
    month_list = create_month_list(
        calendar_settings["Start Date"], calendar_settings["End Date"]
    )

    # Assign colors to the months
    assign_month_colors(month_list, calendar_settings)

    # Generate the images
    days_with_images = create_day_objects(calendar_settings)
    # Assuming days_with_images is already populated with Day objects
    calendar_with_days = create_calendar_with_days(days_with_images, calendar_settings)

    calendar_with_weekdays = add_days_of_week_to_calendar(
        calendar_with_days, calendar_settings
    )

    calendar_with_thick_lines = draw_thick_lines(
        calendar_with_weekdays, calendar_settings, days_with_images, month_list
    )

    calendar_with_months = add_months_to_calendar(
        calendar_with_thick_lines, calendar_settings, days_with_images, month_list
    )

    calendar_with_title = add_calendar_title(calendar_with_months, calendar_settings)

    # Save the calendar image
    calendar_with_title.save("calendar.png")

    calendar_pdf = PDF(
        dpi=calendar_settings["PPI"],
        pixel_width=calendar_settings["Paper Pixel Width"],
        pixel_height=calendar_settings["Paper Pixel Height"],
        doc_width_inch=calendar_settings["Paper Width"],
        doc_height_inch=calendar_settings["Paper Height"],
        margin_inch=calendar_settings["Margin"],
        image_path="calendar.png",
    )

    return calendar_with_title, calendar_pdf


def add_calendar_title(calendar_image, calendar_settings):
    # Calculate the maximum font size for the title
    max_font_size = find_max_font_size(
        calendar_settings["Font Path Title"],
        calendar_settings["Title"],
        calendar_settings["Paper Pixel Width"],
        int(
            calendar_settings["Top Margin Pixels"]
            * calendar_settings["Top Title Proportion"]
        ),
    )

    if max_font_size is None:
        return calendar_image

    # Create a font object with the maximum font size
    title_font = ImageFont.truetype(calendar_settings["Font Path Title"], max_font_size)

    # Estimate the size of the title image (adding extra space for descenders)
    estimated_height = max_font_size * 2  # Extra 20% space for descenders

    # Create a larger transparent image for the title
    title_image_large = Image.new(
        "RGBA",
        (calendar_settings["Paper Pixel Width"], int(estimated_height)),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(title_image_large)

    # Draw the title on the larger transparent image
    draw.text(
        (0, max_font_size * 0.1),
        calendar_settings["Title"],
        fill="black",
        font=title_font,
    )

    # Trim the image to the actual bounding box of the rendered text
    bbox = title_image_large.getbbox()
    title_image = title_image_large.crop(bbox)

    # Save the title image as a PNG for inspection
    title_image.save("title.png")

    # Calculate the position to paste the title image onto the calendar image
    title_width, title_height = title_image.size
    title_x = (calendar_settings["Paper Pixel Width"] - title_width) // 2
    title_y = calendar_settings["Margin Pixels"]
    ic(title_image.getbbox())

    # Paste the title image onto the calendar image
    calendar_image.paste(title_image, (title_x, title_y), title_image)

    ic(calendar_image.size)
    ic(calendar_settings["Paper Pixel Width"], calendar_settings["Paper Pixel Height"])

    return calendar_image
