import pytest
from src.sourcemodel.sm_import import SMImport


# Test initialization of SMImport
def test_sm_import_initialization():
    module_name = "module.name"
    alias = "module_alias"
    is_from_import = True

    sm_import = SMImport(module_name, alias, is_from_import)

    assert sm_import.module_name == module_name, "Module name should be set correctly"
    assert sm_import.alias == alias, "Alias should be set correctly"
    assert sm_import.is_from_import == is_from_import, "Is_from_import should be set correctly"


# Test initialization without optional parameters
def test_sm_import_initialization_without_optional_params():
    module_name = "module.name"

    sm_import = SMImport(module_name)

    assert sm_import.module_name == module_name, "Module name should be set correctly"
    assert sm_import.alias is None, "Alias should be None when not provided"
    assert sm_import.is_from_import is False, "Is_from_import should be False when not provided"
