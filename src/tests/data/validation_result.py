__all__ = ["validation_result_dict"]

validation_result_dict = {
    "isValid": False,
    "detail": [
        {
            "fieldCode": "table_list_1",
            "documentId": "35813",
            "errors": [{"message": "Error message", "column": 0, "row": 0, "index": 1, "kvId": None}],
            "warnings": [{"message": "Warning message", "column": 0, "row": 0, "index": 0, "kvId": None}],
        },
        {
            "fieldCode": "checkbox_1",
            "documentId": "35813",
            "errors": [{"message": "Error message", "column": None, "row": None, "index": None, "kvId": None}],
            "warnings": [],
        },
        {
            "fieldCode": "kv_pair_list_1",
            "documentId": "35813",
            "errors": [
                {"message": "Error message", "column": None, "row": None, "index": 0, "kvId": "value"},
                {"message": "Error message", "column": None, "row": None, "index": 1, "kvId": "key"},
            ],
            "warnings": [],
        },
        {
            "fieldCode": "string_list_1",
            "documentId": "35813",
            "errors": [{"message": "Error message", "column": None, "row": None, "index": 1, "kvId": None}],
            "warnings": [{"message": "Warning message", "column": None, "row": None, "index": 0, "kvId": None}],
        },
        {
            "fieldCode": "string_1",
            "documentId": "35813",
            "errors": [],
            "warnings": [{"message": "Error message", "column": None, "row": None, "index": None, "kvId": None}],
        },
        {
            "fieldCode": "kv_pair_1",
            "documentId": "35813",
            "errors": [
                {"message": "Error message", "column": None, "row": None, "index": None, "kvId": "value"},
                {"message": "Error message", "column": None, "row": None, "index": None, "kvId": "key"},
            ],
            "warnings": [],
        },
    ],
}
