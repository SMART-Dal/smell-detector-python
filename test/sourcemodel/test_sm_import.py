from sourcemodel.sm_import import PyImport


def test_import_initialization():
    pyimport = PyImport("module_name", "alias_name", True)
    assert pyimport.module_name == "module_name"
    assert pyimport.alias == "alias_name"
    assert pyimport.is_from_import


def test_import_without_alias():
    pyimport = PyImport("module_name")
    assert pyimport.module_name == "module_name"
    assert pyimport.alias is None
    assert not pyimport.is_from_import


def test_import_default_is_from_import():
    pyimport = PyImport("module_name", "alias_name")
    assert pyimport.is_from_import == False

