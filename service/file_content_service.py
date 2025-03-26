import xml.sax

from models.db_init import SessionLocal
from models.model import File, Tag, Attribute


class FileContentService(xml.sax.ContentHandler):
    """SAX-обработчик XML-файла для сохранения структуры в базу данных.

    При парсинге сохраняет:
    - имя файла в таблицу File;
    - теги (элементы) в таблицу Tag;
    - атрибуты каждого тега в таблицу Attribute.
    """

    def __init__(self, filename):
        """Инициализация обработчика.

       Args:
           filename (str): Имя XML-файла.
       """
        super().__init__()
        self.filename = filename
        self.session = SessionLocal()
        self.file_id = None

    def startDocument(self):
        """Вызывается один раз в начале документа.
        Сохраняет имя XML-файла в таблицу File.
        """
        new_file = File(name=self.filename)
        self.session.add(new_file)
        self.session.flush()
        self.file_id = new_file.id

    def startElement(self, name, attrs):
        """Вызывается при начале каждого XML-элемента (тега).

       Сохраняет имя тега и все его атрибуты в базу данных.

       Args:
           name (str): Имя тега.
           attrs (xml.sax.xmlreader.AttributesImpl): Атрибуты тега.
       """
        tag = Tag(name=name, file_id=self.file_id)
        self.session.add(tag)
        self.session.flush()

        for attr_name in attrs.getNames():
            attribute = Attribute(
                name=attr_name,
                value=attrs.getValue(attr_name),
                tag_id=tag.id
            )
            self.session.add(attribute)

    def endDocument(self):
        """Вызывается в конце XML-документа.
        Завершает транзакцию и закрывает сессию.
        """
        self.session.commit()
        self.session.close()
