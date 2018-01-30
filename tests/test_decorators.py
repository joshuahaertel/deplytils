"""Test Decorators"""
from unittest import TestCase

from putils.decorators import cached_class_property


# pylint: disable=unused-variable
# noinspection PyMissingOrEmptyDocstring
class TestCachedClassProperty(TestCase):
    """Test Cached Class Property"""
    # pragma pylint: disable=missing-docstring
    def setUp(self):
        # noinspection PyMissingOrEmptyDocstring
        class TestClass(object):
            times_processed = 0

            # pylint: disable=no-self-argument
            # noinspection PyMethodParameters
            @cached_class_property
            def property(cls):
                cls.times_processed += 1
                return cls.times_processed

        self.class_ = TestClass
        self.instance = TestClass()

    def test_cache_skips_processing(self):
        self.assertEqual(self.class_.property, 1)
        self.assertEqual(self.class_.property, 1)
        self.assertEqual(self.class_.times_processed, 1)

    def test_cache_invalidates(self):
        self.assertEqual(self.class_.property, 1)
        del self.class_.property
        self.assertEqual(self.class_.property, 2)
        self.assertEqual(self.class_.property, 2)
        self.assertEqual(self.class_.times_processed, 2)

    def test_instance_has_access(self):
        self.assertEqual(self.instance.property, 1)
        self.assertEqual(self.instance.property, 1)

    def test_full_delete_class_property(self):
        del self.class_.property
        with self.assertRaises(AttributeError):
            del self.class_.property

    def test_delete_property_after_use(self):
        """make sure we can delete class property after using it"""
        self.test_cache_invalidates()
        del self.class_.property
        self.test_full_delete_class_property()
