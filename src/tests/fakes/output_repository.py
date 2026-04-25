from typing import Optional

from deps_output_exporting.domain.model import IOutputRepository, Output

__all__ = ["FakeOutputRepository"]


class FakeOutputRepository(IOutputRepository):
    def __init__(self, fake_db: Optional[dict[str, Output]] = None) -> None:
        self._output_db = {} if fake_db is None else fake_db

    def save(self, output: Output) -> None:
        self._output_db[output.id()] = output

    def find_by_id(self, tenant_id: str, output_id: str) -> Optional[Output]:
        if (output := self._output_db.get(output_id)) and output.tenant_id() == tenant_id:
            return output
        return None

    def find_by_document_id(self, tenant_id: str, document_id: str) -> list[Output]:
        return [
            output
            for output in self._output_db.values()
            if output.tenant_id() == tenant_id and output.document_id == document_id
        ]

    def delete(self, tenant_id: str, document_id: str, output_id: str) -> Optional[Output]:
        outputs = [
            output
            for output in self._output_db.values()
            if all([output.tenant_id() == tenant_id, output.document_id == document_id, output.id() == output_id])
        ]
        if len(outputs) == 1:
            return self._output_db.pop(outputs[0].id(), None)

    def delete_all(self, tenant_id: str, output_ids: list[str]) -> None:
        outputs = [
            output
            for output in self._output_db.values()
            if output.id() in output_ids and output.tenant_id() == tenant_id
        ]
        for output in outputs:
            self._output_db.pop(output.id(), None)

    def delete_outdated_outputs(self, document_id: str, tenant_id: str, profile_id: str) -> list[Output]:
        document_profile_outputs = [
            output
            for output in self._output_db.values()
            if all(
                [
                    output.tenant_id() == tenant_id,
                    output.document_id == document_id,
                    output.profile_info.id() == profile_id,
                ]
            )
        ]
        old_outputs = sorted(document_profile_outputs, key=lambda output: output.creation_date, reverse=True)[1:]
        return [self._output_db.pop(output.id()) for output in old_outputs]
