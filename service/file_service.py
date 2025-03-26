from models.db_init import SessionLocal
from models.model import File, Tag
from response_str import file_not_found, name_not_exist, fill_file_and_tags, \
    tag_not_found
from schemas.save_schemas import SuccessFileSchema, ErrorSchema, CountSchema, \
    AttributesOutSchema
from service.file_content_service import FileContentService
import xml.sax


class FileService:
    """Сервис для работы с XML-файлами и их структурой.

    Предоставляет методы:
    - сохранения содержимого XML-файла в базу данных через SAX-парсинг;
    - получения количества определённых тегов в загруженном файле;
    - получения списка уникальных атрибутов для заданного тега в файле.

    Использует SQLAlchemy-сессию и работает с таблицами File, Tag и Attribute.
    Все методы реализованы как статические.
    """
    @staticmethod
    def save_data(file):
        handler = FileContentService(file.filename)
        xml.sax.parse(file.stream, handler)
        return SuccessFileSchema(success=True).dict()

    @staticmethod
    def get_tag_count(filepath, tag_name):
        if not filepath or not tag_name:
            return ErrorSchema(success=False, error=fill_file_and_tags).dict()
        session = SessionLocal()
        file = session.query(File).filter_by(name=filepath).first()
        if not file:
            return ErrorSchema(success=False, error=file_not_found).dict()

        count = session.query(Tag).filter_by(file_id=file.id,
                                             name=tag_name).count()
        if count == 0:
            return ErrorSchema(success=False, error=name_not_exist).dict()

        return CountSchema(count=count).dict()

    @staticmethod
    def get_tag_attributes(filename, tag_name):
        if not filename or not tag_name:
            return ErrorSchema(success=False, error=fill_file_and_tags).dict()

        session = SessionLocal()
        file = session.query(File).filter_by(name=filename).first()
        if not file:
            return ErrorSchema(success=False, error=fill_file_and_tags).dict()
        tags = session.query(Tag).filter_by(file_id=file.id,
                                            name=tag_name).all()
        if not tags:
            return ErrorSchema(success=False,
                               error=tag_not_found)

        attributes = set()
        for tag in tags:
            for attr in tag.attributes:
                attributes.add(attr.name)
        return AttributesOutSchema(attributes=list(attributes)).dict()
