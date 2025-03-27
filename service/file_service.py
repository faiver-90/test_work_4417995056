from models.db_init import SessionLocal
from response_str import file_not_found, name_not_exist, fill_file_and_tags, \
    tag_not_found
from schemas.schemas import SuccessFileSchema, ErrorSchema, CountSchema, \
    AttributesOutSchema

from service.file_content_service import FileContentService
import xml.sax
from sqlalchemy import text


class FileService:
    """
    Сервис для работы с XML-файлами и их структурой.

    Предоставляет методы:
    - сохранения содержимого XML-файла в базу данных через SAX-парсинг;
    - получения количества определённых тегов в загруженном файле;
    - получения списка уникальных атрибутов для заданного тега в файле.

    Использует SQLAlchemy-сессию и работает с таблицами File, Tag и Attribute.
    Все запросы выполняются через чистый SQL с использованием text().
    """

    @staticmethod
    def save_data(file):
        """
        Сохраняет содержимое XML-файла в базу данных через SAX-парсинг.

        Args:
            file: Загружаемый файл (.xml)

        Returns:
            dict: Успешный результат выполнения
        """
        handler = FileContentService(file.filename)
        xml.sax.parse(file.stream, handler)
        return SuccessFileSchema(success=True).dict()

    @staticmethod
    def get_tag_count(filepath, tag_name):
        """
        Получение количества тегов в файле по имени тега.

        Args:
            filepath: Имя XML-файла
            tag_name: Имя тега для подсчета

        Returns:
            dict: Количество тегов или ошибка
        """
        if not filepath or not tag_name:
            return ErrorSchema(success=False, error=fill_file_and_tags).dict()

        session = SessionLocal()

        file_id_sql = text("SELECT id FROM files WHERE name = :filename")
        file_result = session.execute(file_id_sql,
                                      {"filename": filepath}).first()
        if not file_result:
            return ErrorSchema(success=False, error=file_not_found).dict()

        file_id = file_result[0]

        count_sql = text("""
            SELECT COUNT(*)
            FROM tags
            WHERE file_id = :file_id AND name = :tag_name
        """)
        count = session.execute(count_sql, {"file_id": file_id,
                                            "tag_name": tag_name}).scalar()

        if count == 0:
            return ErrorSchema(success=False, error=name_not_exist).dict()

        return CountSchema(count=count).dict()

    @staticmethod
    def get_tag_attributes(filepath, tag_name):
        """
        Получение уникальных имён атрибутов для заданного тега в указанном файле.

        Args:
            filepath: Имя XML-файла
            tag_name: Имя тега

        Returns:
            dict: Список уникальных атрибутов или ошибка
        """
        if not filepath or not tag_name:
            return ErrorSchema(success=False, error=fill_file_and_tags).dict()

        session = SessionLocal()

        file_id_sql = text("SELECT id FROM files WHERE name = :filename")
        file_result = session.execute(file_id_sql,
                                      {"filename": filepath}).first()
        if not file_result:
            return ErrorSchema(success=False, error=file_not_found).dict()

        file_id = file_result[0]

        tag_ids_sql = text("""
                SELECT id FROM tags
                WHERE file_id = :file_id AND name = :tag_name
            """)
        tag_rows = session.execute(tag_ids_sql, {
            "file_id": file_id,
            "tag_name": tag_name
        }).fetchall()

        if not tag_rows:
            return ErrorSchema(success=False, error=tag_not_found).dict()

        tag_ids = [row[0] for row in tag_rows]

        if not tag_ids:
            return AttributesOutSchema(attributes=[]).dict()

        placeholders = ', '.join([f":id_{i}" for i in range(len(tag_ids))])
        params = {f"id_{i}": tag_id for i, tag_id in enumerate(tag_ids)}

        attributes_sql = text(f"""
                SELECT DISTINCT name
                FROM attributes
                WHERE tag_id IN ({placeholders})
            """)
        attributes_result = session.execute(attributes_sql, params).fetchall()
        attributes = [row[0] for row in attributes_result]

        return AttributesOutSchema(attributes=attributes).dict()
