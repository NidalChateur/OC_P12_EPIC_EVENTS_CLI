from src.models.department import Department
from src.utils.slugify import slugify
from tests import MixinSetup


class TestDepartment(MixinSetup):
    def test_french_name(self):
        assert Department.FRENCH_NAME == "département"

    def test_str(self):
        self.clear_db()
        department = self.create_department("Gestion")

        assert str(department) == department.name.capitalize()

    def test_rpr(self):
        department = self.session.get(Department, 1)

        assert str(department) == repr(department)

    def test_save(self):
        department = self.session.get(Department, 1)
        department.save(self.session)

        assert department.slug == f"{department.id}-{slugify(department.name)}"
