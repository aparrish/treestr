from __future__ import print_function
import unittest

from treestr import treestr as t


class TreestrTest(unittest.TestCase):
    def test_singles(self):
        # just assume that if "upper()" works, the rest will too
        src = t("hello")
        dest = src.upper()
        self.assertEqual(type(src), t)
        self.assertEqual(type(dest), t)
        self.assertEqual(dest, "HELLO")
        self.assertIn(src, dest.parents)

    def test_getitem(self):
        src = t("magnolia")
        substr = src[1:-1]
        self.assertEqual(substr, "agnoli")
        self.assertIn(src, substr.parents)

    def test_parents_from_args(self):
        src = t("hello")
        fillch = t("*")
        dest = src.center(25, fillch)
        self.assertIn(src, dest.parents)
        self.assertIn(fillch, dest.parents)

    def test_add(self):
        one = t("hello")
        two = t("there")
        three = one + two
        self.assertEqual(three, "hellothere")
        self.assertIn(one, three.parents)
        self.assertIn(two, three.parents)

    def test_add_with_str(self):
        one = t("hello")
        two = "there"
        three = one + two
        self.assertEqual(three, "hellothere")
        self.assertIsInstance(three, t)

    def test_radd(self):
        one = "hello"
        two = t("there")
        three = one + two
        self.assertEqual(three, "hellothere")
        self.assertIsInstance(three, t)

    def test_mul(self):
        src = t("hello")
        dest = src * 5
        self.assertEqual(dest, "hellohellohellohellohello")
        self.assertIsInstance(dest, t)

    def test_rmul(self):
        src = t("hello")
        dest = 5 * src
        self.assertEqual(dest, "hellohellohellohellohello")
        self.assertIsInstance(dest, t)

    def test_partition(self):
        src = t("it was the best of times, it was the worst of times")
        a, b, c = src.partition(', ')
        self.assertEqual(a, "it was the best of times")
        self.assertEqual(b, ", ")
        self.assertEqual(c, "it was the worst of times")
        self.assertIsInstance(a, t)
        self.assertIsInstance(b, t)
        self.assertIsInstance(c, t)
        self.assertIn(src, a.parents)
        self.assertIn(src, b.parents)
        self.assertIn(src, c.parents)

    def test_split(self):
        src = t("a test")
        a, b = src.split(" ")
        self.assertEqual(a, "a")
        self.assertEqual(b, "test")
        self.assertIsInstance(a, t)
        self.assertIsInstance(b, t)
        self.assertIn(src, a.parents)
        self.assertIn(src, b.parents)

    def test_join(self):
        sep = t(", ")
        one = t("hello")
        two = t("there")
        three = sep.join([one, two])
        self.assertEqual(three, "hello, there")
        self.assertEqual(set(three.parents), set([sep, one, two]))

    def test_mod(self):
        tmpl = t("this is a %s")
        fill_in = t("test")
        result = tmpl % (fill_in,)
        self.assertEqual(result, "this is a test")
        self.assertIsInstance(result, t)
        self.assertIn(tmpl, result.parents)
        self.assertIn(fill_in, result.parents)
        result = tmpl % fill_in
        self.assertEqual(result, "this is a test")
        self.assertIsInstance(result, t)
        self.assertIn(tmpl, result.parents)
        self.assertIn(fill_in, result.parents)

    def test_format(self):
        tmpl = t("this is a {0}")
        fill_in = t("test")
        result = tmpl.format(fill_in)
        self.assertEqual(result, "this is a test")
        self.assertIsInstance(result, t)
        self.assertIn(tmpl, result.parents)
        self.assertIn(fill_in, result.parents)

    def test_rtags(self):
        a = t("one", tags={'test1'})
        b = t("two", tags={'test2'})
        c = t("three", tags={'test3'}, parents=(a, b))
        d = t("four", parents=(c,))
        self.assertEqual(d.rtags(), {'test1', 'test2', 'test3'})

if __name__ == '__main__':
    unittest.main()
