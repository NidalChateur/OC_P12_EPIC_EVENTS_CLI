from src.models.company import Company
from src.utils.slugify import slugify
from tests import MixinSetup


class TestCompany(MixinSetup):
    def test_french_name(self):
        assert Company.FRENCH_NAME == "entreprise"

    def test_str(self):
        self.clear_db()
        company = Company(name="Apple")
        company.create(self.session)

        assert str(company) == company.name.capitalize()

    def test_rpr(self):
        company = self.session.get(Company, 1)

        assert str(company) == repr(company)

    def test_save(self):
        company = self.session.get(Company, 1)
        company.save(self.session)

        assert company.slug == f"{company.id}-{slugify(company.name)}"
