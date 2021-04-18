import PIL
from arcade import Color
from arcade import Texture, Sprite


def make_hexagon_texture(diameter: int, color: Color, points: list, color_outline="#918585",
                         width_outline=5) -> Texture:
    resize = 4  # resize hack for pillow to antialias image
    bg_color = (0, 0, 0, 0)  # fully transparent

    img = PIL.Image.new("RGBA", (diameter * 2 * resize, diameter * 2 * resize), bg_color)
    draw = PIL.ImageDraw.Draw(img)
    # shift to center and resize
    points = [(resize * (pair[0] + diameter), resize * (pair[1] + diameter)) for pair in points]

    draw.polygon(xy=points, fill=color)

    draw.line(points + list(points[0]), fill=color_outline, width=width_outline)
    img = img.resize((diameter * 2, diameter * 2), resample=PIL.Image.ANTIALIAS)
    name = "{}:{}:{}".format("hexagon_texture", diameter, color)  # name must be unique for caching
    return Texture(name, img)