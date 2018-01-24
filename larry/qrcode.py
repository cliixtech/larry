import base64
import qrcode
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

IMAGE_MODE = 'L'
BACK_COLOR = 'white'

class QRCode(object):
    DATA_URI_FORMAT = "data:%s;base64,%s"
    BYTES_DECODER = 'utf-8'
    IMAGE_FORMAT = 'png'
    IMAGE_MIME_TYPE = 'image/png'
    ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_L
    BOX_SIZE = 10
    BORDER = 4
    ROCKET_PASS = 'https://www.rocketpass.io'

    def __init__(self, content, label=None):
        """
        Create a qrcode with the content and
        label at footer.

        :param content:The content to be stored at qrcode.
        :type content: str.

        :param label: A option label to draw at qrcode footer.
            If None the label will be the rocket pass web site url.
        :type label: :py:class: `dot.qrcode.QRCodeLabel`.

        """
        self._qrcode = qrcode.QRCode(
            version=None,
            error_correction=self.ERROR_CORRECTION,
            box_size=self.BOX_SIZE,
            border=self.BORDER
        )

        if not label:
            label = QRCodeLabel(self.ROCKET_PASS)

        self._qrcode.add_data(content)
        self._qrcode.make(fit=True)
        self._label = label
        self._label.offset = self._get_label_offset()

    def get_data_uri(self):
        """
        Create a data uri representation of this qrcode.

        :returns: The data uri representation
        :rtype: str.

        """
        b64bytes = base64.b64encode(self._get_image_bytes())
        string_data = b64bytes.decode(self.BYTES_DECODER)
        return self.DATA_URI_FORMAT % (self.IMAGE_MIME_TYPE, string_data)

    @property
    def image_bytes(self):
        return self._get_image_bytes()

    @property
    def data_uri(self):
        return self.get_data_uri()

    def _get_image(self):
        qrc_img = self._get_qrcode_image()
        label_img = self._label._get_image()

        qrc_img_with_label = self._vconcat_images(
            [qrc_img, label_img]
        )

        return qrc_img_with_label

    def _get_image_bytes(self):
        img = self._get_image()
        img_buffer = io.BytesIO()
        img.save(img_buffer, self.IMAGE_FORMAT)

        return img_buffer.getvalue()

    def _get_qrcode_image(self):
        qrc_img_wrapper = self._qrcode.make_image()
        return qrc_img_wrapper.get_image()

    def _get_label_offset(self):
        border_width = self.BORDER * self.BOX_SIZE
        return (border_width, 0)

    @staticmethod
    def _vconcat_images(images):
        widths = [img.size[0] for img in images]
        heights = [img.size[1] for img in images]

        width = max(widths)
        height = sum(heights)
        size = (width, height)

        result_image = Image.new(IMAGE_MODE, size, BACK_COLOR)

        paste_x = 0
        paste_y = 0

        for img in images:
            paste_pos = (paste_x, paste_y)
            result_image.paste(img, paste_pos)
            paste_y += img.size[1]

        return result_image

class QRCodeLabel(object):
    FONT_FILE = "assets/fonts/CaviarDreams/Caviar Dreams Bold.ttf"
    FONT_SIZE = 10
    FONT_COLOR = 'black'
    DEFAULT_TEXT = ' '
    SPACE_BEWEEN_LINES = 0
    POS_ORIGIN = (0, 0)

    def __init__(self, text=None, font_file=None):
        """
        Create a label with the given text.

        :param text: The text to be draw at label.
        :type text: str.

        :param font_file: A path to a true type or open type font
        :type font_file: str.

        """
        if not text:
            text = self.DEFAULT_TEXT

        self._lines = self._prepare_lines(text)
        self._offset = None
        self._font_size = None
        self._font_file = font_file

    @property
    def offset(self):
        """
        Returns the value of the offset that will
        be applied at label text.

        :returns: A tuple defining (width, height).
        :rtype: 2-tuple (int, int).

        """
        return self._offset if self._offset else self.POS_ORIGIN

    @offset.setter
    def offset(self, value):
        """
        Set a new value to the label offset.

        :param value: A tuple defining (width, height).
        :type value: 2-tuple (int, int).

        """
        self._offset = value

    @property
    def font_size(self):
        """
        """
        if not self._font_file:
            raise AttributeError("Only exists if a font_file was especified")

        return self._font_size if self._font_size else self.FONT_SIZE

    @font_size.setter
    def font_size(self, value):
        """
        Set a new value to the text font size.

        :param value: The size to apply at text font size.
        :type value: int.

        """
        if not self._font_file:
            raise AttributeError("Only exists if a font_file was especified")

        self._font_size = value

    def _get_image(self):
        img = Image.new(
            IMAGE_MODE,
            self._get_image_size(),
            BACK_COLOR
        )

        draw = ImageDraw.Draw(img)
        draw.multiline_text(
            self.offset,
            self._get_text_to_draw(),
            font=self._get_font(),
            fill=self.FONT_COLOR,
            spacing=self.SPACE_BEWEEN_LINES
        )

        return img

    @staticmethod
    def _prepare_lines(text):

        def empty_to_blank(text):
            return text if text else ' '

        lines = text.splitlines()
        lines = [empty_to_blank(l) for l in lines]
        return lines

    def _get_text_to_draw(self):
        return "\n".join(self._lines)

    def _get_image_size(self):
        font = self._get_font()
        lines = self._lines
        lines_size = [font.getsize(line) for line in lines]
        lines_width = [size[0] for size in lines_size]
        lines_height = [size[1] for size in lines_size]

        width = max(lines_width)
        height = sum(lines_height)

        width += self.offset[0]
        height += self.offset[1]
        height += len(lines) * self.SPACE_BEWEEN_LINES

        return (width, height)

    def _get_font(self):
        if self._font_size:
            return ImageFont.truetype(self._font_file, self.font_size)

        return ImageFont.load_default()
