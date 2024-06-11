import os.path
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import arabic_reshaper
from bidi.algorithm import get_display
import cv2
import textwrap


def is_arabic_or_english(text) -> str:
    # Compile a regular expression to match Arabic and English characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF]+')  # Arabic range
    english_pattern = re.compile(r'[a-zA-Z]+')  # English range

    # Check if the text contains Arabic or English characters
    if arabic_pattern.search(text):
        return "ar"
    elif english_pattern.search(text):
        return "en"


def remove_numbers(text):
    # Compile a regular expression to match any digit
    numbers = re.findall(r'\d', text)
    digit_pattern = re.compile(r'\d')

    # Replace all digits with an empty string
    text_without_numbers = digit_pattern.sub('', text)

    return text_without_numbers


def arabic(text):
    return get_display(arabic_reshaper.reshape(text))


def design1(poster_img, title: str, episodenum ,platform, genre, desc) -> str:
    
    img  = cv2.imread(poster_img)
    mask = cv2.imread('layers/mask.png',0)
    img = cv2.resize(img, (2000, 2000))

    result1 = img.copy()
    result1[mask == 0] = 0
    result1[mask != 0] = img[mask != 0]

    

    cv2.imwrite('layers/masked.png', result1)

    img = Image.open("layers/masked.png").convert("RGBA")
    red = Image.open("layers/redwithlogo.png").convert("RGBA")
    bar = Image.open("layers/redbar.png").convert("RGBA")
    bluebackground = Image.open("layers/bluebackground.png").convert("RGBA")
    bottomShadow1 = Image.open("layers/bottomShadow.png").convert("RGBA")
    bottomShadow2 = Image.open("layers/bottomShadow2.png").convert("RGBA")
    episode = Image.open("layers/episode.png").convert("RGBA")
    devices = Image.open("layers/devices.png").convert("RGBA")


    img.paste(bluebackground, (0, 0), bluebackground)
    img.paste(red, (0, 0), red)
    img.paste(bottomShadow2, (0,0), bottomShadow2)
    img.paste(bottomShadow1, (0, 0), bottomShadow1)
    img.paste(bar, (0,0), bar)
    img.paste(episode, (0,-9), episode)
    img.paste(devices, (0,0), devices)
    
    
    titlepos = (720, 1400)
    genrepos = (730, 1750)
    platformpos  = (1500, 1830)
    episodepos = (1640,210)
    qatar_font = "design/qatar.ttf"
    arabic_font = "design/arabic.otf"



    draw = ImageDraw.Draw(img)

    title_kind = is_arabic_or_english(title)
    title = title.strip()
    
    words = title.split(" ")
    if len(words) == 2:
        titlepos = (610, 1400)
    elif len(words) == 3:
        titlepos = (370, 1400)

    if title_kind == "ar":
        title = arabic(remove_numbers(title))
        # Draw the category text on the image
        draw.text(titlepos, title, font=ImageFont.truetype(arabic_font, 120), fill=(211, 8, 5),
                  align="center")

    else:
        title = remove_numbers(title).replace(".", " ")
        # Draw the category text on the image
        draw.text(titlepos, title, font=ImageFont.truetype(qatar_font, 100), fill=(211, 8, 5),
                  align="center")
        






    platform = arabic(remove_numbers(platform))
    draw.text(platformpos, platform, font=ImageFont.truetype(arabic_font, 60), fill=(255, 255, 255),
                  align="center")
    

    if len(str(episodenum)) == 1:
        episodepos = (1650,210)
        draw.text(episodepos, str(episodenum), font=ImageFont.truetype(qatar_font, 80), fill=(211, 8, 5),
                  align="center")
    elif len(str(episodenum)) == 3:
        episodepos = (1610,210)
        draw.text(episodepos, str(episodenum), font=ImageFont.truetype(qatar_font, 80), fill=(211, 8, 5),
                  align="center")
    elif len(str(episodenum)) == 4:
        episodepos = (1592,210)
        draw.text(episodepos, str(episodenum), font=ImageFont.truetype(qatar_font, 80), fill=(211, 8, 5),
                  align="center")
    else:
        draw.text(episodepos, str(episodenum), font=ImageFont.truetype(qatar_font, 80), fill=(211, 8, 5),
                align="center")

    
    genre = arabic(remove_numbers(genre))
    
    words = genre.split("-")
    print(words)
    if len(words) == 4:
        genre = str(words[0] + "-" + words[1] + "\n\n" + words[2] + "-" + words[3])
        draw.text(genrepos, str(genre), font=ImageFont.truetype(arabic_font, 70), fill=(211, 8, 5),
                  align="center")
    elif len(words) == 2:
        draw.text(genrepos, str(genre), font=ImageFont.truetype(arabic_font, 70), fill=(211, 8, 5),
                   align="center")
    else:
         genrepos = (900, 1750)
         draw.text(genrepos, str(genre), font=ImageFont.truetype(arabic_font, 70), fill=(211, 8, 5),
                 align="center")



    desc = arabic(remove_numbers(desc))
    if len(desc) < 124 and len(desc) > 62:
        desc = textwrap.wrap(desc, width=62)
        descpos = (300,  1550)
        draw.text(descpos, desc[1] + "\n\n"+ desc[0], font=ImageFont.truetype(arabic_font, 50), fill=(255, 255, 255),
                  align="center")
    else:
        descpos = (300, 1550)
        draw.text(descpos, str(desc), font=ImageFont.truetype(arabic_font, 50), fill=(255, 255, 255),
                align="center")

    # Save the final image
    img.save("final.png",format="png")

    return os.path.abspath("final.png")


if __name__ == '__main__':
    design1(
        poster_img="poster.png",
        title="title",
        episodenum=13,
        platform="platform",
        genre="genre",
        desc="desc"
    )
