from ...base_serializer import ConfiguredBaseModel
from ..dto import Line, LineElement, Paragraph

__all__ = ["SerializedParagraph"]


class SerializedWord(ConfiguredBaseModel):
    content: str

    def to_model(self) -> LineElement:
        return LineElement(content=self.content)


class SerializedSelectionMark(ConfiguredBaseModel):
    state: str

    def to_model(self) -> LineElement:
        return LineElement(content=self.state)


class SerializedBarcodeFormulaSignature(ConfiguredBaseModel):
    value: str

    def to_model(self) -> LineElement:
        return LineElement(content=self.value)


class SerializedLine(ConfiguredBaseModel):
    content: str
    words: list[SerializedWord]
    selection_marks: list[SerializedSelectionMark]
    barcodes: list[SerializedBarcodeFormulaSignature]
    formulas: list[SerializedBarcodeFormulaSignature]
    signatures: list[SerializedBarcodeFormulaSignature]

    def to_model(self) -> Line:
        elements = []
        for elem_list in (self.words, self.selection_marks, self.barcodes, self.formulas, self.signatures):
            elements.extend([elem.to_model() for elem in elem_list])
        return Line(
            content=self.content,
            elements=elements,
        )


class SerializedParagraph(ConfiguredBaseModel):
    content: str
    lines: list[SerializedLine]

    def to_model(self) -> Paragraph:
        return Paragraph(content=self.content, lines=[line.to_model() for line in self.lines])
