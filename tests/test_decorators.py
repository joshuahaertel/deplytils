from unittest import TestCase

from putils.decorators import cached_class_property


class TestCachedClassProperty(TestCase):
    def setUp(self):
        class TestClass(object):
            times_processed = 0

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
