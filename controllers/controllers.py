from flask import Blueprint, request

from response_str import file_not_found, format_xml
from schemas.save_schemas import ErrorSchema
from service.file_service import FileService

bp = Blueprint('files', __name__)


@bp.route('/test')
def index():
    """Проверка доступности сервера.

    Возвращает простое текстовое сообщение, подтверждающее,
    что сервер и подключение к SQLite работают.
    """
    return 'Flask + SQLite работает!'


@bp.route('/api/file/read', methods=['POST'])
def save_data():
    """Загрузка и парсинг XML-файла.

    Принимает XML-файл через form-data под ключом 'file'.
    Сохраняет имя файла, теги и атрибуты в базу данных.
    Используется SAX-парсинг.

    Returns:
        SuccessFileSchema (success=True) — если всё прошло успешно.
        ErrorSchema — если файл не найден, неверный формат или ошибка парсинга.
        """
    if 'file' not in request.files:
        return ErrorSchema(success=False, error=file_not_found).dict()

    file = request.files['file']
    if not file.filename.endswith('.xml'):
        return ErrorSchema(success=False, error=format_xml).dict()

    try:
        return FileService().save_data(file)
    except Exception as e:
        return ErrorSchema(success=False, error=str(e)).dict()


@bp.route('/api/tags/get-count', methods=['GET'])
def get_tag_count():
    """Получение количества тегов по имени в конкретном файле.

      Query-параметры:
          file: str — имя загруженного XML-файла.
          tag: str — имя тега для подсчёта.

      Returns:
          CountSchema — количество найденных тегов.
          ErrorSchema — если файл или тег не найден.
      """
    filepath = request.args.get('file')
    tag_name = request.args.get('tag')
    try:
        return FileService().get_tag_count(filepath, tag_name)
    except Exception as e:
        return ErrorSchema(success=False, error=str(e)).dict()


@bp.route('/api/tags/attributes/get', methods=['GET'])
def get_tag_attributes():
    """Получение уникальных имён атрибутов указанного тега в XML-файле.

    Query-параметры:
        file: str — имя файла.
        tag: str — имя тега, у которого нужно получить атрибуты.

    Returns:
        AttributesOutSchema — список имён атрибутов (без повторов).
        ErrorSchema — если файл или тег не найден.
    """
    filename = request.args.get('file')
    tag_name = request.args.get('tag')
    try:
        return FileService().get_tag_attributes(filename, tag_name)
    except Exception as e:
        return ErrorSchema(success=False, error=str(e)).dict()
