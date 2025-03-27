import xml.sax

from sqlalchemy import text

from models.db_init import SessionLocal


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
        insert_file_sql = text("""
                   INSERT INTO files (name)
                   VALUES (:filename)
                   RETURNING id
               """)
        result = self.session.execute(insert_file_sql,
                                      {"filename": self.filename})
        self.file_id = result.scalar_one()  # Получаем ID вставленного файла

    def startElement(self, name, attrs):
        """Вызывается при начале каждого XML-элемента (тега).

       Сохраняет имя тега и все его атрибуты в базу данных.

       Args:
           name (str): Имя тега.
           attrs (xml.sax.xmlreader.AttributesImpl): Атрибуты тега.
       """
        insert_tag_sql = text("""
            INSERT INTO tags (name, file_id)
            VALUES (:tag_name, :file_id)
            RETURNING id
        """)
        result = self.session.execute(insert_tag_sql, {
            "tag_name": name,
            "file_id": self.file_id
        })
        tag_id = result.scalar_one()

        # 2. Сохраняем атрибуты тега
        for attr_name in attrs.getNames():
            insert_attr_sql = text("""
                INSERT INTO attributes (name, value, tag_id)
                VALUES (:name, :value, :tag_id)
            """)
            self.session.execute(insert_attr_sql, {
                "name": attr_name,
                "value": attrs.getValue(attr_name),
                "tag_id": tag_id
            })

    def endDocument(self):
        """Вызывается в конце XML-документа.
        Завершает транзакцию и закрывает сессию.
        """
        self.session.commit()
        self.session.close()
