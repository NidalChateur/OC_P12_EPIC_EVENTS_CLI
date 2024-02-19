from src.models.location import Location, slugify, unfilled
from tests import MixinSetup


class TestLocation(MixinSetup):
    def test_french_name(self):
        assert Location.FRENCH_NAME == "lieu"

    def test_str(self):
        self.clear_db()
        location = self.create_location()

        assert str(location) == f"{location.zip_code} {location.city}"

        location.name = "Tour Eiffel"
        location.number = "5"
        location.street_type = "Avenue"
        location.street_name = "Anatole France"

        name = location.name
        number = location.number
        street = f"{location.street_type} {location.street_name}"

        assert (
            str(location)
            == f"{name}, {number} {street}, {location.zip_code} {location.city}"
        )

    def test_formatted_name(self):
        location = self.session.get(Location, 1)
        location.name = "centre ville de Paris"

        assert location.formatted_name == "centre ville de Paris".title()

        location.name = ""

        assert location.formatted_name == unfilled

    def test_formatted_address(self):
        location = self.session.get(Location, 1)

        assert location.formatted_address == location.__str__(name=False)

    def test_save(self):
        location = self.session.get(Location, 1)
        location.save(self.session)

        assert location.slug == f"{location.id}-{slugify(str(location))}"
