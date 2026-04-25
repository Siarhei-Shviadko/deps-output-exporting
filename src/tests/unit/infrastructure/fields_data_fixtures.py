import pytest

from deps_output_exporting.infrastructure.proxies import (
    Cell,
    Coordinates,
    ExtractedField,
    FieldType,
    GenericData,
    KeyValuePairData,
    TableData,
    ValidationResult,
)

__all__ = [
    "fields_data__all_fields_with_validation",
    "fields_data__some_fields_all_valid",
    "fields_data__some_fields_without_validation",
    "fields_data__table_field",
]


@pytest.fixture
def fields_data__all_fields_with_validation():
    return [
        ExtractedField(
            code="checkbox_1",
            data=GenericData(
                value=True,
                confidence=0.9748279618539318,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.FAILED,
            ),
            name="Checkbox 1",
            type=FieldType.CHECKMARK,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="checkbox_list_1",
            data=[
                GenericData(
                    value=True,
                    confidence=0.9770115448508438,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
                GenericData(
                    value=False,
                    confidence=0.8094946106916409,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
                GenericData(
                    value=None,
                    confidence=0.8583335635072465,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
            ],
            name="Checkbox list 1",
            type=FieldType.LIST,
            base_type=FieldType.CHECKMARK,
            page=1,
        ),
        ExtractedField(
            code="enum_1",
            data=GenericData(
                value="3b65e7c495004646bd567e333946154c",
                confidence=0.8612308813121231,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.PASSED,
            ),
            name="Enum 1",
            type=FieldType.ENUM,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="enum_list_1",
            data=[
                GenericData(
                    value="48262c4c407a45f098195bf293b3de28",
                    confidence=0.8746645939599489,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
                GenericData(
                    value="f",
                    confidence=0.9216453483103249,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
            ],
            name="Enum list 1",
            type=FieldType.LIST,
            base_type=FieldType.ENUM,
            page=1,
        ),
        ExtractedField(
            code="kv_pair_1",
            data=KeyValuePairData(
                key=GenericData(
                    value="985a37dfb6b34d8082e6157c7e1b86fd",
                    confidence=0.9934127164610282,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.FAILED,
                ),
                value=GenericData(
                    value="0c197676253f44a89f882eb7296b1861",
                    confidence=0.8583414171040242,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.FAILED,
                ),
            ),
            name="Key-Value Pair 1",
            type=FieldType.DICT,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="kv_pair_list_1",
            data=[
                KeyValuePairData(
                    key=GenericData(
                        value="c7ebd9f27d834143b8d809aa42ea20ca",
                        confidence=0.9387609186786404,
                        source_id="53fefdf433704cbcb346c65c266746ba",
                        validation_result=ValidationResult.PASSED,
                    ),
                    value=GenericData(
                        value="9bca244a30ff4a02a995f0f870b66d30",
                        confidence=0.919873358732982,
                        source_id="53fefdf433704cbcb346c65c266746ba",
                        validation_result=ValidationResult.FAILED,
                    ),
                ),
                KeyValuePairData(
                    key=GenericData(
                        value="564b27777f1b41949bad51bdbd573f51",
                        confidence=0.9108412046527585,
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.FAILED,
                    ),
                    value=GenericData(
                        value="4bf46332fb454229b6428941242c48e8",
                        confidence=0.9340049024356571,
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                ),
            ],
            name="Key-Value Pair list 1",
            type=FieldType.LIST,
            base_type=FieldType.DICT,
            page=1,
        ),
        ExtractedField(
            code="string_1",
            data=GenericData(
                value="Bunting",
                confidence=0.9223522186279297,
                source_id="e6d8da65e4a64dc488a59b4982b269aa",
                validation_result=ValidationResult.PASSED,
            ),
            name="String 1",
            type=FieldType.STRING,
            base_type=None,
            page=2,
        ),
        ExtractedField(
            code="string_list_1",
            data=[
                GenericData(
                    value="780bc476656c4597916b367287e0105f",
                    confidence=0.8640509710142759,
                    source_id="e6d8da65e4a64dc488a59b4982b269aa",
                    validation_result=ValidationResult.PASSED,
                ),
                GenericData(
                    value="0cd034a6b87242b5a0f1d8f8e624ac03",
                    confidence=0.8386486916662136,
                    source_id="e6d8da65e4a64dc488a59b4982b269aa",
                    validation_result=ValidationResult.FAILED,
                ),
                GenericData(
                    value="bea8da5b61e842a581e3a3e1b3f3fac8",
                    confidence=0.8914050646624923,
                    source_id="e6d8da65e4a64dc488a59b4982b269aa",
                    validation_result=ValidationResult.PASSED,
                ),
            ],
            name="String list 1",
            type=FieldType.LIST,
            base_type=FieldType.STRING,
            page=2,
        ),
        ExtractedField(
            code="table_1",
            data=TableData(
                row_count=2,
                column_count=2,
                cells=[
                    Cell(
                        value="dfdbc8f0bf624bb7b4cccfc65d01a060",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=0,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    )
                ],
                header_row=["Col1", "Col2"],
            ),
            name="Table 1",
            type=FieldType.TABLE,
            base_type=None,
            page=2,
        ),
        ExtractedField(
            code="table_list_1",
            data=[
                TableData(
                    row_count=2,
                    column_count=2,
                    cells=[
                        Cell(
                            value="6ac94d17d3764f9583ed9325d40e3948",
                            confidence=0.8604765306324114,
                            coordinates=Coordinates(
                                column_index=0,
                                row_index=0,
                                colspan=1,
                                rowspan=1,
                            ),
                            source_id="e6d8da65e4a64dc488a59b4982b269aa",
                            validation_result=ValidationResult.PASSED,
                        ),
                    ],
                    header_row=["Col1", "Col2"],
                ),
                TableData(
                    row_count=2,
                    column_count=2,
                    cells=[
                        Cell(
                            value="16fa5884783647e6a4e1dc0f46b0c330",
                            confidence=0.9822785996834371,
                            coordinates=Coordinates(
                                column_index=0,
                                row_index=0,
                                colspan=1,
                                rowspan=1,
                            ),
                            source_id="e6d8da65e4a64dc488a59b4982b269aa",
                            validation_result=ValidationResult.FAILED,
                        )
                    ],
                    header_row=["Col1", "Col2"],
                ),
            ],
            name="Table list 1",
            type=FieldType.LIST,
            base_type=FieldType.TABLE,
            page=2,
        ),
        ExtractedField(
            code="string_2",
            data=GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED),
            name="String 2",
            type=FieldType.STRING,
            base_type=None,
            page=None,
        ),
        ExtractedField(
            code="kv_pair_2",
            data=KeyValuePairData(
                key=GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED),
                value=GenericData(
                    value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED
                ),
            ),
            name="Key-Value Pair 2",
            type=FieldType.DICT,
            base_type=None,
            page=None,
        ),
        ExtractedField(
            code="checkbox_2",
            data=GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED),
            name="Checkbox 2",
            type=FieldType.CHECKMARK,
            base_type=None,
            page=None,
        ),
        ExtractedField(
            code="enum_2",
            data=GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED),
            name="Enum 2",
            type=FieldType.ENUM,
            base_type=None,
            page=None,
        ),
        ExtractedField(
            code="string_list_2",
            data=[GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED)],
            name="String list 2",
            type=FieldType.LIST,
            base_type=FieldType.STRING,
            page=None,
        ),
        ExtractedField(
            code="kv_pair_list_2",
            data=[
                KeyValuePairData(
                    key=GenericData(
                        value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED
                    ),
                    value=GenericData(
                        value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED
                    ),
                )
            ],
            name="Key-Value Pair list 2",
            type=FieldType.LIST,
            base_type=FieldType.DICT,
            page=None,
        ),
        ExtractedField(
            code="checkbox_list_2",
            data=[GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED)],
            name="Checkbox list 2",
            type=FieldType.LIST,
            base_type=FieldType.CHECKMARK,
            page=None,
        ),
        ExtractedField(
            code="enum_list_2",
            data=[GenericData(value=None, confidence=None, source_id=None, validation_result=ValidationResult.PASSED)],
            name="Enum list 2",
            type=FieldType.LIST,
            base_type=FieldType.ENUM,
            page=None,
        ),
    ]


@pytest.fixture
def fields_data__some_fields_without_validation():
    return [
        ExtractedField(
            code="checkbox_1",
            data=GenericData(
                value=True,
                confidence=0.9748279618539318,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.NOT_APPLIED,
            ),
            name="Checkbox 1",
            type=FieldType.CHECKMARK,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="enum_1",
            data=GenericData(
                value="3b65e7c495004646bd567e333946154c",
                confidence=0.8612308813121231,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.NOT_APPLIED,
            ),
            name="Enum 1",
            type=FieldType.ENUM,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="kv_pair_1",
            data=KeyValuePairData(
                key=GenericData(
                    value="985a37dfb6b34d8082e6157c7e1b86fd",
                    confidence=0.9934127164610282,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.NOT_APPLIED,
                ),
                value=GenericData(
                    value="0c197676253f44a89f882eb7296b1861",
                    confidence=0.8583414171040242,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.NOT_APPLIED,
                ),
            ),
            name="Key-Value Pair 1",
            type=FieldType.DICT,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="string_1",
            data=GenericData(
                value="Bunting",
                confidence=0.9223522186279297,
                source_id="e6d8da65e4a64dc488a59b4982b269aa",
                validation_result=ValidationResult.NOT_APPLIED,
            ),
            name="String 1",
            type=FieldType.STRING,
            base_type=None,
            page=2,
        ),
        ExtractedField(
            code="table_1",
            data=TableData(
                row_count=2,
                column_count=2,
                cells=[
                    Cell(
                        value="dfdbc8f0bf624bb7b4cccfc65d01a060",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=0,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.NOT_APPLIED,
                    )
                ],
                header_row=["Col1", "Col2"],
            ),
            name="Table 1",
            type=FieldType.TABLE,
            base_type=None,
            page=2,
        ),
    ]


@pytest.fixture
def fields_data__table_field():
    return [
        ExtractedField(
            code="table_1",
            data=TableData(
                row_count=3,
                column_count=3,
                cells=[
                    Cell(
                        value="val1",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=0,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                    Cell(
                        value="val2",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=1,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                    Cell(
                        value="val3",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=2,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                    Cell(
                        value="val4",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=0,
                            row_index=1,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                    Cell(
                        value="val5",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=1,
                            row_index=1,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                    Cell(
                        value="val6",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=2,
                            row_index=1,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    ),
                ],
                header_row=["Col1", "Col2", "Col3"],
            ),
            name="Table 1",
            type=FieldType.TABLE,
            base_type=None,
            page=1,
        ),
    ]


@pytest.fixture
def fields_data__some_fields_all_valid():
    return [
        ExtractedField(
            code="checkbox_1",
            data=GenericData(
                value=True,
                confidence=0.9748279618539318,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.PASSED,
            ),
            name="Checkbox 1",
            type=FieldType.CHECKMARK,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="enum_1",
            data=GenericData(
                value="3b65e7c495004646bd567e333946154c",
                confidence=0.8612308813121231,
                source_id="53fefdf433704cbcb346c65c266746ba",
                validation_result=ValidationResult.PASSED,
            ),
            name="Enum 1",
            type=FieldType.ENUM,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="kv_pair_1",
            data=KeyValuePairData(
                key=GenericData(
                    value="985a37dfb6b34d8082e6157c7e1b86fd",
                    confidence=0.9934127164610282,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
                value=GenericData(
                    value="0c197676253f44a89f882eb7296b1861",
                    confidence=0.8583414171040242,
                    source_id="53fefdf433704cbcb346c65c266746ba",
                    validation_result=ValidationResult.PASSED,
                ),
            ),
            name="Key-Value Pair 1",
            type=FieldType.DICT,
            base_type=None,
            page=1,
        ),
        ExtractedField(
            code="string_1",
            data=GenericData(
                value="Bunting",
                confidence=0.9223522186279297,
                source_id="e6d8da65e4a64dc488a59b4982b269aa",
                validation_result=ValidationResult.PASSED,
            ),
            name="String 1",
            type=FieldType.STRING,
            base_type=None,
            page=2,
        ),
        ExtractedField(
            code="table_1",
            data=TableData(
                row_count=2,
                column_count=2,
                cells=[
                    Cell(
                        value="dfdbc8f0bf624bb7b4cccfc65d01a060",
                        confidence=0.8033054327046043,
                        coordinates=Coordinates(
                            column_index=0,
                            row_index=0,
                            colspan=1,
                            rowspan=1,
                        ),
                        source_id="e6d8da65e4a64dc488a59b4982b269aa",
                        validation_result=ValidationResult.PASSED,
                    )
                ],
                header_row=["Col1", "Col2"],
            ),
            name="Table 1",
            type=FieldType.TABLE,
            base_type=None,
            page=2,
        ),
    ]
