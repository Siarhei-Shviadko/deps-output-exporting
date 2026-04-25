__all__ = ["json_dl_output_all_features", "json_dl_output_one_feature", "json_dl_output_with_key_values"]

json_dl_output_all_features = {
    "pages": [
        {
            "page_number": 1,
            "tables": [
                {
                    "column_count": 2,
                    "row_count": 1,
                    "cells": [
                        {
                            "content": "QUANTITY",
                            "column_index": 0,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "columnHeader",
                        },
                        {
                            "content": "DESCRIPTION",
                            "column_index": 1,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "columnHeader",
                        },
                    ],
                }
            ],
            "key_value_pairs": [{"Phone": "(243) 758-4368"}, {"Fax": "(243) 758-5839"}],
            "paragraphs": [
                {"content": "Header", "lines": [{"content": "Header", "elements": [{"content": "Header"}]}]}
            ],
        },
        {
            "page_number": 2,
            "tables": [
                {
                    "column_count": 2,
                    "row_count": 1,
                    "cells": [
                        {
                            "content": "SUBTOTAL",
                            "column_index": 0,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "content",
                        },
                        {
                            "content": "$2,100.00",
                            "column_index": 1,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "content",
                        },
                    ],
                }
            ],
            "key_value_pairs": [{"INVOICE NO:": "2491839"}, {"DATE:": "24/06/2019"}],
            "paragraphs": [
                {"content": "INVOICE", "lines": [{"content": "INVOICE", "elements": [{"content": "INVOICE"}]}]}
            ],
        },
        {
            "page_number": 3,
            "tables": [],
            "key_value_pairs": [],
            "paragraphs": [],
        },
    ]
}

json_dl_output_one_feature = {
    "pages": [
        {
            "page_number": 1,
            "key_value_pairs": [{"Phone": "(243) 758-4368"}, {"Fax": "(243) 758-5839"}],
        },
        {"page_number": 2, "key_value_pairs": [{"INVOICE NO:": "2491839"}, {"DATE:": "24/06/2019"}]},
    ]
}

json_dl_output_with_key_values = {
    "pages": [
        {
            "page_number": 1,
            "tables": [
                {
                    "column_count": 2,
                    "row_count": 1,
                    "cells": [
                        {
                            "content": "QUANTITY",
                            "column_index": 0,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "columnHeader",
                        },
                        {
                            "content": "DESCRIPTION",
                            "column_index": 1,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "columnHeader",
                        },
                    ],
                }
            ],
            "key_value_pairs": [{"Phone": "(243) 758-4368"}, {"Fax": "(243) 758-5839"}],
            "paragraphs": [
                {"content": "Header", "lines": [{"content": "Header", "elements": [{"content": "Header"}]}]}
            ],
        },
        {
            "page_number": 2,
            "tables": [
                {
                    "column_count": 2,
                    "row_count": 1,
                    "cells": [
                        {
                            "content": "SUBTOTAL",
                            "column_index": 0,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "content",
                        },
                        {
                            "content": "$2,100.00",
                            "column_index": 1,
                            "row_index": 0,
                            "column_span": 1,
                            "row_span": 1,
                            "kind": "content",
                        },
                    ],
                }
            ],
            "key_value_pairs": [{"INVOICE NO:": "2491839"}, {"DATE:": "24/06/2019"}],
            "paragraphs": [
                {"content": "INVOICE", "lines": [{"content": "INVOICE", "elements": [{"content": "INVOICE"}]}]}
            ],
        },
        {
            "page_number": 3,
            "tables": [],
            "key_value_pairs": [],
            "paragraphs": [],
        },
    ],
    "key_values": [
        {
            "key": "In viverra",
            "value": "Aliquam erat volutpat. Fusce vel viverra eros. Etiam lectus turpis, pellentesque sit amet porta nec, dapibus et ipsum. Donec gravida urna id varius interdum. Aenean luctus volutpat mi, in accumsan tortor pretium sit amet. Nullam ante sapien, malesuada id ante accumsan, efficitur elementum arcu. Nunc diam dui, suscipit et arcu nec, vulputate lacinia tortor. Vestibulum vehicula turpis nec enim volutpat malesuada pretium at sapien. Quisque at interdum lorem, eget iaculis neque. Fusce sed leo sem. In lorem purus, consequat faucibus malesuada sit amet, auctor eu massa. Etiam fermentum dui quis orci pretium rhoncus.",
        },
        {
            "key": "Sed semper finibus",
            "value": "Quisque vulputate mi et massa tristique lacinia. Quisque non fermentum metus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis porta interdum nunc at consectetur. Pellentesque non aliquet eros. Donec ac sem vel enim consequat accumsan vel sit amet nunc. Vestibulum sit amet commodo sapien, et sollicitudin diam. Donec id placerat neque, eu dictum augue. Sed dapibus mauris nisl, non dignissim augue porttitor ac. Ut vitae iaculis urna, eu scelerisque eros. Nunc feugiat dolor elementum, feugiat dui eget, vehicula tortor.",
        },
    ],
}
