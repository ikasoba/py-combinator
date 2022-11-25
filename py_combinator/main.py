import re
import typing

T = typing.TypeVar("T")

IgnoreParserFunc = typing.Callable[[int, str], typing.Tuple[int, T, typing.Literal["ignore"]] | None]
_ParserFunc = typing.Callable[[int, str], typing.Tuple[int, T] | None]
ParserFunc = typing.Union[IgnoreParserFunc[T], _ParserFunc[T]]

def token(pattern: str | re.Pattern) -> ParserFunc[str]:
    def f(i: int, s: str):
        if isinstance(pattern, re.Pattern):
            m = pattern.match(s, i)
            if not m: return None
            groups = m.groups()
            i += len(m.group())
            return (i, groups[0] if len(groups) else m.group())
        else:
            return (i + len(pattern), pattern) if s.startswith(pattern, i) else None
    return f

def ignore(parser: ParserFunc[T]) -> IgnoreParserFunc[T]:
    def f(i: int, s: str):
        m = parser(i, s)
        return (m[0], m[1], True) if m else None
    return f

def join(*parsers: ParserFunc[T]) -> ParserFunc[list[T]]:
    def f(i: int, s: str):
        res = []
        for parser in parsers:
            m = parser(i, s)
            if not m: return None
            i = m[0]
            if not (len(m) >= 3 and typing.cast(list[typing.Any], m)[2] != "ignore"):
                res.append(m[1])
        return i, res
    return f

def some(*parsers: ParserFunc[T]) -> ParserFunc[T]:
    def f(i: int, s: str):
        for parser in parsers:
            m = parser(i, s)
            if not m: continue
            i = m[0]
            return i, m[1]
        return None
    return f