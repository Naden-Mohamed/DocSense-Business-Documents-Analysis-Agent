from typing import cast
from fastapi import APIRouter
from core.config import get_settings, Settings
from fastapi import APIRouter, UploadFile, Depends, status, Request
from models.enums.responce_status import ResponseStatus
from db.document_model import DocumentModel
from models.api_responce import APIResponce
from services.data_service import DocumentParserService
from models.db_schemes.document import Document
from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)

data = APIRouter(tags = ['api/data'], prefix = "/data")

@data.post('/upload')
async def upload_file(request:Request, file: UploadFile) ->  APIResponce:
    db_client = request.app.state.db_client
    doc_model =  DocumentModel(db_client)
    document_model = await doc_model.get_instance(db_client)
    data_service = DocumentParserService()
    is_valid , result_signal =  data_service.validate_uploaded_file(file=file)
    if not is_valid:
        return APIResponce(status_code=status.HTTP_400_BAD_REQUEST, status=result_signal,error="File uploaded is not valid")

    try:
        doc = Document(
            _id=ObjectId(),
            doc_name=file.filename,
            doc_type=file.content_type,
            doc_metadata={},
            doc_path=file.filename,
            num_pages=file.size
        )
        result = await doc_model.upload_document(doc=doc)
    except Exception as e:
        logger.exception("File upload fail")
        return APIResponce(status_code=status.HTTP_400_BAD_REQUEST, status=ResponseStatus.FILE_UPLOAD_FAILED.value,error="File upload failed")

    return APIResponce(status_code=status.HTTP_200_OK, status= ResponseStatus.FILE_UPLOADED_SUCCESSFULLY.value)

