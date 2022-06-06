from PIL import Image


def image_autorotate(infile):
    print(infile)
    image = Image.open(infile)
    exif = image._getexif()

    # if image has exif data about orientation, let's rotate it
    orientation_key = 274  # cf ExifTags
    if exif and orientation_key in exif:
        orientation = exif[orientation_key]

        rotate_values = {
            3: Image.ROTATE_180,
            6: Image.ROTATE_270,
            8: Image.ROTATE_90
        }

        if orientation in rotate_values:
            image = image.transpose(rotate_values[orientation])

    return image
