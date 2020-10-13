from PIL import Image, ImageDraw, ImageFont

class ElementDrawer():

    @staticmethod
    def drawRectangule(originalImage:Image, limits:list, color:str) -> Image:

        editedImage = ImageDraw.Draw(originalImage)
        editedImage.rectangle(xy=limits, outline=color)

        return editedImage

    @staticmethod
    def drawTextBox(originalImage:Image, txt:str, fontType:str, limits:list, color:str) -> Image:

        font = ImageFont.truetype(fontType, 15)
        textSize = font.getsize(txt)
        editedImage = ImageDraw.Draw(originalImage)
        
        textLocation = [limits[0] + 2., limits[1] - textSize[1]]
        textboxLocation = [limits[0], limits[1] - textSize[1], limits[0] + textSize[0] + 4., limits[1]]

        editedImage.rectangle(xy=textboxLocation, fill=color)
        editedImage.text(xy=textLocation, text=txt, fill='white', font=font)

        return editedImage
