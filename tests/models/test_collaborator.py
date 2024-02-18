from src.models.collaborator import Collaborator, unfilled
from src.utils.fernet import Fernet
from src.utils.slugify import slugify
from tests import MixinSetup


class TestCollaborator(MixinSetup):
    def test_french_name(self):
        assert Collaborator.FRENCH_NAME == "collaborateur"

    def test_str(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert str(obj) == f"{obj.first_name.capitalize()} {obj.last_name.capitalize()}"

    def test_repr(self):
        obj = self.session.get(Collaborator, 1)

        assert str(obj) == repr(obj)

    def test_name(self):
        obj = self.session.get(Collaborator, 1)

        assert str(obj) == obj.name

    def test_formatted_phone(self):
        obj = self.session.get(Collaborator, 1)

        assert obj.formatted_phone == " ".join(
            [obj.phone[i : i + 2] for i in range(0, len(obj.phone), 2)]
        )

        obj.phone = ""
        assert obj.formatted_phone == unfilled

    def test_prompt_phone(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.prompt_phone == obj.phone

        obj.phone = ""
        assert obj.prompt_phone == ""

    def test_slug_first_name(self):
        obj = self.session.get(Collaborator, 1)

        assert obj.slug_first_name == slugify(obj.first_name)

    def test_slug_last_name(self):
        obj = self.session.get(Collaborator, 1)

        assert obj.slug_last_name == slugify(obj.last_name)

    def test_prompt_department(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.prompt_department == str(obj.department)

        obj.department = None
        assert obj.prompt_department == ""

    def test_role(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.role == str(obj.department)

        obj.department = None
        assert obj.role == unfilled

    def test_title(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.title == f"{obj.role} {obj.first_name.capitalize()}"

    def test_formatted_birthdate(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.formatted_birthdate == obj.birthdate.strftime("%d/%m/%Y")

    def test_prompt_birthdate(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.prompt_birthdate == obj.birthdate.strftime("%Y-%m-%d")

    def test_slug_role(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj._slug_role == obj.department.slug_name

        obj.department = None
        assert obj._slug_role == ""

    def test_hash_password(self):
        assert Collaborator._hash_password(self.CLEAR_PASSWORD) != self.CLEAR_PASSWORD

    def test_set_password(self):
        self.clear_db()
        obj = self.create_collaborator("Gestion")

        assert obj.password is None

        obj.set_password(self.CLEAR_PASSWORD)

        assert obj.password is not None
        assert obj.password != self.CLEAR_PASSWORD

    def test_get_with_clear_email(self):
        collaborator = Collaborator.get_with_clear_email(self.session, self.CLEAR_EMAIL)

        assert collaborator is not None
        assert Fernet.decrypt(collaborator.email) == self.CLEAR_EMAIL

    def test_check_password(self):
        collaborator = self.session.get(Collaborator, 1)

        assert Collaborator.check_password(self.CLEAR_PASSWORD, collaborator.password)

        assert Collaborator.check_password("different", collaborator.password) is False
        assert Collaborator.check_password(None, collaborator.password) is False

    def test_authenticate(self):
        collaborator = self.session.get(Collaborator, 1)

        assert collaborator.last_login is None

        authenticated = Collaborator.authenticate(
            self.session, self.CLEAR_EMAIL, self.CLEAR_PASSWORD
        )

        assert authenticated == collaborator
        assert authenticated.last_login is not None

    def test_save(self):
        obj = self.session.get(Collaborator, 1)
        obj.save(self.session)

        slug = f"{obj.id}-{obj.slug_first_name}-{obj.slug_last_name}-{obj._slug_role}"

        assert obj.slug == slug

    def test_delete(self):
        obj = self.session.get(Collaborator, 1)
        obj.delete(self.session)

        assert self.session.get(Collaborator, 1) is None
