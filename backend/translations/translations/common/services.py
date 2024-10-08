from translations.config.settings.storages import MEDIA_ROOT
import uuid
import os


def text_to_local_file_upload(
    *, file_name: str, content: str, extension: str = ".txt"
) -> str:
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    file_path = os.path.join(MEDIA_ROOT, f"{file_name}{extension}")

    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def file_get_local_content(*, file_name: str) -> str:
    file_path = os.path.join(MEDIA_ROOT, file_name)
    with open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()


def content_get_local_translation(*, content: str, language: str) -> str:
    return f"{content[:10]}... to {language}"


def file_name_generate(extension: str = ".txt") -> str:
    unique_id = uuid.uuid4()
    hex_filename = unique_id.hex

    return f"{hex_filename}{extension}"
