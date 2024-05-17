import datetime

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from pytz import timezone

from service.util import special_logger
from service.weather import weather_files, WeatherData

tz = timezone("US/Eastern")


IMAGES_DIR = "images/"
FONTS_DIR = "fonts/"
GENERATED_DIR = "generated/"
STATIC_DIR = "static/"
CALENDAR_DATA = "generated/calendar_data"
PERSISTENT_DIR = "persistent/"


class BannerMaker:
    def __init__(self, banner_id):
        self.banner_id = banner_id

    def replace_banner(
        self, weather: WeatherData, calendar: str = " ", message: str = " "
    ):
        currently_icon = weather.currently_icon

        now = datetime.date.strftime(datetime.datetime.now(tz), "%a %-I:%M%p")

        summary = f"{now} {weather.summary} {weather.temp}"

        font_size_in_points = 9
        font = ImageFont.truetype(FONTS_DIR + "led.ttf", font_size_in_points)
        font_size = font.getsize(summary)
        special_logger(
            f"summary: {summary}, font size: {font_size} calendar:"
            f" {calendar}, message: {message}"
        )
        summary_img = Image.new("RGB", font_size)
        draw = ImageDraw.Draw(summary_img)
        main_fill_color = "#ffffff" if weather.is_daytime else "#ff0000"

        draw.text((0, 0), summary, font=font, fill=main_fill_color)
        enh = ImageEnhance.Contrast(summary_img)
        enh.enhance(1.99).save(GENERATED_DIR + "enh.ppm")

        enhanced_summary = Image.open(GENERATED_DIR + "enh.ppm")

        current_img = Image.open(f"{IMAGES_DIR}{weather_files[currently_icon]}")

        if message:
            font_size = font.getsize(message)
            message_img = Image.new("RGB", font_size)
            message_draw = ImageDraw.Draw(message_img)
            message_draw.text((0, 0), message, font=font, fill="GreenYellow")
            enh_message = ImageEnhance.Contrast(message_img)
            enh_message.enhance(1.99).save(GENERATED_DIR + "messagetext.ppm")
            enhanced_message = Image.open(GENERATED_DIR + "messagetext.ppm")
            message_width = enhanced_message.width
        else:
            message_width = 0

        font_size = font.getsize(calendar)
        calendar_img = Image.new("RGB", font_size)
        calendar_draw = ImageDraw.Draw(calendar_img)
        calendar_draw.text((0, 0), calendar, font=font, fill="cyan")
        enh_calendar = ImageEnhance.Contrast(calendar_img)
        enh_calendar.enhance(1.99).save(GENERATED_DIR + "calendartext.ppm")

        enhanced_calendar = Image.open(GENERATED_DIR + "calendartext.ppm")

        size = (
            enhanced_summary.width
            + current_img.width
            + enhanced_calendar.width
            + message_width,
            16,
        )

        banner = Image.new("RGB", size)
        banner.paste(enhanced_summary, (0, 4))

        if weather.is_daytime:
            # show weather icon when it's daytime
            banner.paste(current_img, (enhanced_summary.width, 0))

            # NOTE: Shows rainbow when it's daytime
            colors = ["red", "orange", "yellow", "green", "blue", "purple"]
            for i, color in enumerate(colors):
                stripe = Image.new("RGB", (enhanced_summary.width, 1), color)
                banner.paste(stripe, (0, i if i < 3 else i + 10))

        banner.paste(enhanced_calendar, (enhanced_summary.width + current_img.width, 4))

        if message:
            banner.paste(
                enhanced_message,
                (
                    enhanced_summary.width
                    + current_img.width
                    + enhanced_calendar.width,
                    4,
                ),
            )

        led_output_file_name = f"weather{self.banner_id}.ppm"
        web_output_file_name = f"display{self.banner_id}.jpg"

        banner.save(GENERATED_DIR + led_output_file_name)
        banner.save(STATIC_DIR + led_output_file_name)
        self.export_jpg(
            GENERATED_DIR + led_output_file_name, PERSISTENT_DIR + web_output_file_name
        )

    @staticmethod
    def export_jpg(ppmFilePath, outputFilePath):
        im = Image.open(ppmFilePath)
        im.save(outputFilePath)
