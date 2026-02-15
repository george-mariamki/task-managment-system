from app.crud.base import CRUDBase
from app.models.attachment import Attachment
from app.schemas.task import AttachmentOut # Neu: Importieren des Schemas für die Ausgabe von Attachments

class CRUDAttachment(CRUDBase[Attachment, AttachmentOut, AttachmentOut]):
    pass

attachment = CRUDAttachment(Attachment)
