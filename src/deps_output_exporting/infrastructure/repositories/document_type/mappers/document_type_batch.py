from deps_output_exporting.domain.model import DocumentType

from .document_type import DocumentTypeMapper

__all__ = ["DocumentTypeBatchMapper"]


class DocumentTypeBatchMapper:
    @classmethod
    def to_dicts(cls, document_types: list[DocumentType]) -> tuple:
        raw_document_types = []
        raw_profiles = []

        for document_type in document_types:
            raw_document_type = DocumentTypeMapper.to_dict(document_type)
            profiles = raw_document_type.pop("profiles")
            raw_document_types.append(raw_document_type)
            raw_profiles.extend(profiles)

        return raw_document_types, raw_profiles
