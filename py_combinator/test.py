import unittest
import re
import main as combinator

class TestToken(unittest.TestCase):
    def test_string(self):
        self.assertEqual(
            combinator.token("hogehoge")(0, "hogehoge"),
            (8, "hogehoge")
        )

    def test_regex(self):
        self.assertEqual(
            combinator.token(re.compile("(?:hoge|fuga)+"))(0, "fugahogefugafugahoge"),
            (20, "fugahogefugafugahoge")
        )

class TestJoin(unittest.TestCase):
    def test_string(self):
        self.assertEqual(
            combinator.join(
                combinator.token("hogehoge"),
                combinator.token("fugafuga")
            )(0, "hogehogefugafuga"),
            (16, ["hogehoge", "fugafuga"])
        )

    def test_regex(self):
        self.assertEqual(
            combinator.join(
                combinator.token(re.compile("(?:hoge)+")),
                combinator.token(re.compile("(?:fuga)+"))
            )(0, "hogehogefuga"),
            (12, ["hogehoge", "fuga"])
        )

    def test_regex_and_string(self):
        self.assertEqual(
            combinator.join(
                combinator.token(re.compile("(?:hoge)+")),
                combinator.token("fuga")
            )(0, "hogehogehogefuga"),
            (16, ["hogehogehoge", "fuga"])
        )

class TestSome(unittest.TestCase):
    def test_string(self):
        self.assertEqual(
            combinator.some(
                combinator.token("hoge"),
                combinator.token("fuga")
            )(0, "fuga"),
            (4, "fuga")
        )

    def test_regex(self):
        self.assertEqual(
            combinator.some(
                combinator.token(re.compile("(?:hoge)+")),
                combinator.token(re.compile("(?:fuga)+"))
            )(0, "fugafuga"),
            (8, "fugafuga")
        )

    def test_regex_and_string(self):
        self.assertEqual(
            combinator.some(
                combinator.token(re.compile("(?:hoge)+")),
                combinator.token("fuga")
            )(0, "hogehogehoge"),
            (12, "hogehogehoge")
        )

class TestIgnore(unittest.TestCase):
    def test_join(self):
        self.assertEqual(
            combinator.join(
                combinator.ignore(combinator.token(re.compile("(?:hoge)+"))),
                combinator.token("fuga")
            )(0, "hogehogehogefuga"),
            (16, ["fuga"])
        )

if __name__ == '__main__':
    unittest.main()