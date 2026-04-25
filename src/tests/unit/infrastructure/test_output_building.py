import json

from deps_output_exporting.domain.model import Output
from deps_output_exporting.infrastructure.external_storages import (
    OneDriveStorage,
    SalesforceStorage,
)
from deps_output_exporting.infrastructure.services import (
    ExcelDataBuilder,
    OutputBuildingService,
)
from tests.data import json_edata_output_all_fields, json_edata_output_some_fields


class TestOutputBuildingService:
    FILEPATH = "output/"

    def test_build_edata_json_output__all_fields__built(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_json_all_fields,
        document_type__edata_json_all_fields_profile,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        file_name_json,
        upload_json_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_json)

        output = output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_json_all_fields,
            document_type__edata_json_all_fields_profile.id(),
        )

        upload_json_file_mock.assert_called_with(
            self.FILEPATH, file_name_json, json.dumps(json_edata_output_all_fields).encode("utf8")
        )

        assert isinstance(output, Output)
        assert output.tenant_id() == test_tenant_id
        assert output.profile_info.id == profile__edata_json_all_fields.id
        assert output.profile_info.version == profile__edata_json_all_fields.version
        assert output.document_id == document_id
        assert output.state == "ready"
        assert output.file_path == f"{self.FILEPATH}{file_name_json}"
        assert output.creation_date

    def test_build_edata_json_output__no_fields_profile__built_with_all_fields(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_json_no_fields,
        document_type__no_fields_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        file_name_json,
        upload_json_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_json)

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_json_no_fields,
            document_type__no_fields_profiles.id(),
        )

        upload_json_file_mock.assert_called_with(self.FILEPATH, file_name_json, json.dumps({}).encode("utf8"))

    def test_build_edata_json_output__some_fields__built(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_json_some_fields,
        document_type__edata_json_some_fields_profile,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        file_name_json,
        upload_json_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_json)

        output = output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_json_some_fields,
            document_type__edata_json_some_fields_profile.id(),
        )

        upload_json_file_mock.assert_called_with(
            self.FILEPATH, file_name_json, json.dumps(json_edata_output_some_fields).encode("utf8")
        )

        assert isinstance(output, Output)
        assert output.tenant_id() == test_tenant_id
        assert output.profile_info.id == profile__edata_json_some_fields.id
        assert output.profile_info.version == profile__edata_json_some_fields.version
        assert output.document_id == document_id
        assert output.state == "ready"
        assert output.file_path == f"{self.FILEPATH}{file_name_json}"
        assert output.creation_date

    def test_build_edata_excel_output__all_fields_with_validation_results__data_created(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_all_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        fields_data__all_fields_with_validation,
        general_info,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_all_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        create_excel_data.assert_called_with(general_info, fields_data__all_fields_with_validation)

    def test_build_edata_excel_output__no_fields_profile__built_with_all_fields(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_no_fields,
        document_type__no_fields_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        fields_data__all_fields_with_validation,
        general_info__no_fields_profile,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_no_fields,
            document_type__no_fields_profiles.id(),
        )

        create_excel_data.assert_called_with(general_info__no_fields_profile, [])

    def test_build_edata_excel_output__no_fields_default_profile__built_with_all_fields(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_default_no_fields,
        document_type__no_fields_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        fields_data__all_fields_with_validation,
        general_info,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_default_no_fields,
            document_type__no_fields_profiles.id(),
        )

        create_excel_data.assert_called_with(general_info, fields_data__all_fields_with_validation)

    def test_build_edata_excel_output__some_fields_with_validation_results__no_validation__data_created(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_some_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_not_found_request_mock,
        fields_data__some_fields_without_validation,
        general_info__some_fields_with_validation_results,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_some_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        create_excel_data.assert_called_with(
            general_info__some_fields_with_validation_results, fields_data__some_fields_without_validation
        )

    def test_build_edata_excel_output__some_fields_without_validation_results__data_created(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_some_fields_without_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        fields_data__some_fields_without_validation,
        general_info__some_fields_with_validation_results,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_some_fields_without_validation,
            document_type__edata_excel_profiles.id(),
        )

        create_excel_data.assert_called_with(
            general_info__some_fields_with_validation_results, fields_data__some_fields_without_validation
        )

    def test_build_edata_excel_output__some_fields_with_validation_results__all_valid__data_created(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_some_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock__all_valid,
        fields_data__some_fields_all_valid,
        general_info__some_fields_with_validation_results,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_some_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        create_excel_data.assert_called_with(
            general_info__some_fields_with_validation_results, fields_data__some_fields_all_valid
        )

    def test_build_output__salesforce_info__file_passed_to_uploading(
        self,
        output_building_service,
        test_tenant_id,
        profile__salesforce_info,
        document_type__profiles_with_external_storages,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        mocker,
        mocked_file_storage_request,
        mocked_output_service_file_name_generator,
        generated_name_json,
    ):
        salesforce_uploading = mocker.patch.object(SalesforceStorage, "upload")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__salesforce_info,
            document_type__profiles_with_external_storages.id(),
        )

        salesforce_uploading.assert_called_with(
            generated_name_json,
            json.dumps(json_edata_output_some_fields).encode("utf8"),
            profile__salesforce_info.external_storages_info[0],
        )

    def test_build_output__onedrive_info__file_passed_to_uploading(
        self,
        output_building_service,
        test_tenant_id,
        profile__onedrive_info,
        document_type__profiles_with_external_storages,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        mocker,
        mocked_file_storage_request,
        mocked_output_service_file_name_generator,
        generated_name_json,
    ):
        onedrive_uploading = mocker.patch.object(OneDriveStorage, "upload")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__onedrive_info,
            document_type__profiles_with_external_storages.id(),
        )

        onedrive_uploading.assert_called_with(
            generated_name_json,
            json.dumps(json_edata_output_some_fields).encode("utf8"),
            profile__onedrive_info.external_storages_info[0],
        )

    def test_build_output__salesforce_and_onedrive_info__file_passed_to_uploading(
        self,
        output_building_service,
        test_tenant_id,
        profile__salesforce_onedrive_info,
        document_type__profiles_with_external_storages,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        mocker,
        mocked_file_storage_request,
        mocked_output_service_file_name_generator,
        generated_name_json,
    ):
        salesforce_uploading = mocker.patch.object(SalesforceStorage, "upload")
        onedrive_uploading = mocker.patch.object(OneDriveStorage, "upload")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__salesforce_onedrive_info,
            document_type__profiles_with_external_storages.id(),
        )

        salesforce_uploading.assert_called_with(
            generated_name_json,
            json.dumps(json_edata_output_some_fields).encode("utf8"),
            profile__salesforce_onedrive_info.external_storages_info[0],
        )
        onedrive_uploading.assert_called_with(
            generated_name_json,
            json.dumps(json_edata_output_some_fields).encode("utf8"),
            profile__salesforce_onedrive_info.external_storages_info[1],
        )

    def test_build_edata_excel_output__engine_in_document_detail__passed_to_builder(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_all_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_all_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        assert create_excel_data.call_args.args[0].engine == "TESSERACT"

    def test_build_edata_excel_output__engine_in_document_type__passed_to_builder(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_all_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock,
        get_document_success_request_mock__no_engine,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_all_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        assert create_excel_data.call_args.args[0].engine == "TESSERACT"

    def test_build_edata_excel_output__default_engine__passed_to_builder(
        self,
        output_building_service,
        test_tenant_id,
        profile__edata_excel_all_fields_with_validation,
        document_type__edata_excel_profiles,
        document_id,
        get_extracted_data_success_request_mock,
        get_document_type_success_request_mock__no_engine,
        get_document_success_request_mock__no_engine,
        get_unifier_success_request_mock,
        get_validation_success_request_mock,
        file_name_excel,
        upload_excel_file_mock,
        mocker,
    ):
        mocker.patch.object(OutputBuildingService, "_generate_file_name", return_value=file_name_excel)
        create_excel_data = mocker.patch.object(ExcelDataBuilder, "with_info")

        output_building_service.build(
            document_id,
            test_tenant_id,
            profile__edata_excel_all_fields_with_validation,
            document_type__edata_excel_profiles.id(),
        )

        assert create_excel_data.call_args.args[0].engine == "TESSERACT"
