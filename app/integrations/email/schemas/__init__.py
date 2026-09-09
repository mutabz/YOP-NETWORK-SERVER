from .email import (
    EmailCreate,
    EmailResponse,
    EmailListItem,
)

from .email_recipient import (
    EmailRecipientCreate,
    EmailRecipientResponse,
)

from .email_attachment import (
    EmailAttachmentCreate,
    EmailAttachmentResponse,
)

from .email_template import (
    EmailTemplateCreate,
    EmailTemplateUpdate,
    EmailTemplatePublishRequest,
    EmailTemplateResponse,
    EmailTemplateListItem,
)

from .email_template_version import (
    EmailTemplateVersionCreate,
    EmailTemplateVersionResponse,
    EmailTemplateVersionListItem,
)

from .email_send_job import (
    EmailSendJobCreate,
    EmailSendJobResponse,
    EmailSendJobListItem,
)


__all__ = [
    # Email
    "EmailCreate",
    "EmailSendRequest",
    "EmailResponse",
    "EmailListItem",

    # Recipients
    "EmailRecipientCreate",
    "EmailRecipientResponse",

    # Attachments
    "EmailAttachmentCreate",
    "EmailAttachmentResponse",

    # Templates
    "EmailTemplateCreate",
    "EmailTemplateUpdate",
    "EmailTemplatePublishRequest",
    "EmailTemplateResponse",
    "EmailTemplateListItem",

    # Template Versions
    "EmailTemplateVersionCreate",
    "EmailTemplateVersionResponse",
    "EmailTemplateVersionListItem",

    # Send Jobs
    "EmailSendJobCreate",
    "EmailSendJobResponse",
    "EmailSendJobListItem",
]