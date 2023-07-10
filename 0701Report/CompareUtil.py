
import collections.abc
import difflib
import os
from typing import AbstractSet
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Sequence
import pprint
import reprlib
from typing import Any,Union
from typing import Dict
from typing import IO
from typing import Optional
from collections import Counter
from difflib import SequenceMatcher

"""
Copyright Holger Krekel and others, 2004.

Distributed under the terms of the MIT license, pytest is free and open source software.

Modify by VictorYang 2023,add other code
"""



def compare_arrays_ignore_order(array1, array2)->tuple[bool,str]:
    """
    function used to compare two arrays ignore order
    :param array1:
    :param array2:
    :return:
    :example:
    array1 = [1, 2, 3, 4, 4, 5]
    array2 = [5, 2, 3, 4, 4, 5]

    ret, diff_info= compare_arrays_ignore_order(array1, array2)
     ==>ret:    False
    ==>diff_info:['Expected: [1] !=  Actual: []',
                'Expected: 2 ==  Actual: 2',
                'Expected: 3 ==  Actual: 3',
                'Expected: 4 ==  Actual: 4',
                'Expected: [5] !=  Actual: [5, 5]']

    """
    counter1 = Counter(array1)
    counter2 = Counter(array2)
    all_elements = set(array1).union(set(array2))  # 所有出现过的元素
    ret = True
    diff_info = []
    for element in all_elements:
        count1 = counter1.get(element, 0)
        count2 = counter2.get(element, 0)
        if count1 == count2:
            diff_info.append((element, "==",element))
        else:
            diff_info.append((count1 * [element],"!=",count2 * [element]))
            if ret:
                ret = False
    explanation = []
    for diff in diff_info:
        explanation.append(f"Expected: {diff[0]} {diff[1]}  Actual: {diff[2]}")
    return ret,explanation

def get_diff_info(left:Any, right:Any)->List[str]:
    """
    function used to print the difference
    :param left:
    :param right:
    :return:List of the differ info
    :example:
        get_diff_info("AB", "CD")
        return ==>AB != CD
        get_diff_info( bytearray([0x01,0x02]),  bytearray([0x02,0x02]))
        return ==>bytearray(b'\x01') != None
                  bytearray(b'\x02') == bytearray(b'\x02')
    """
    matcher = SequenceMatcher(None, left, right)
    opcodes = matcher.get_opcodes()
    explanation = []
    # get the difference
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            #
            explanation.append(f"{left[i1:i2]} == {right[j1:j2]}")
        elif tag == 'delete':
            # 删除部分
            explanation.append(f"{left[i1:i2]} != None")
        elif tag == 'insert':
            # 插入部分
            explanation.append(f"None!= {right[j1:j2]}")
        elif tag == 'replace':
            # 替换部分
            explanation.append(f"{left[i1:i2]} != {right[j1:j2]}")
    return explanation

def get_diff_with_index(left, right):
    """
     function used to print the difference, and will show the index of the element
     :param left:
     :param right:
     :return:List of the differ info with the index of element
     :example:
        get_diff_with_index("AB", "CD")
        ==>A != C (left index: 0, right index: 0)
           B != D (left index: 1, right index: 1)
        get_diff_with_index( bytearray([0x01,0x02]),  bytearray([0x02,0x02]))
        ==>
            1 != None (left index: 0, right index: -)
            2 == 2 (left index: 1, right index: 0)
            None != 2 (left index: -, right index: 1)
     """
    matcher = SequenceMatcher(None, left, right)
    opcodes = matcher.get_opcodes()
    explanation = []
    # get the difference
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                explanation.append(f"{left[i]} == {right[j]} (left index: {i}, right index: {j})")
        elif tag == 'delete':
            for i in range(i1, i2):
                explanation.append(f"{left[i]} != None (left index: {i}, right index: -)")
        elif tag == 'insert':
            for j in range(j1, j2):
                explanation.append(f"None != {right[j]} (left index: -, right index: {j})")
        elif tag == 'replace':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                explanation.append(f"{left[i]} != {right[j]} (left index: {i}, right index: {j})")
    return explanation


def compare_eq_any_explanation(left: Any, right: Any) -> List[str]:
    explanation = []
    if istext(left) and istext(right):
        explanation = _compare_eq_text(left,right)
    if type(left) == type(right) and (
        isdatacls(left) or isattrs(left) or isnamedtuple(left)
    ):
        explanation = _compare_eq_cls(left, right)
    elif issequence(left) and issequence(right):
        explanation = _compare_eq_sequence(left, right)
    elif isset(left) and isset(right):
        explanation = _compare_eq_set(left, right)
    elif isdict(left) and isdict(right):
        explanation = _compare_eq_dict(left, right)


    if isiterable(left) and isiterable(right):
        expl = _compare_eq_iterable(left, right)
        explanation.extend(expl)

    return explanation

def compare_eq_any(left: Any, right: Any) -> List[str]:
    explanation = []
    if istext(left) and istext(right):
        explanation = _compare_eq_text(left,right)
    if type(left) == type(right) and (
            isdatacls(left) or isattrs(left) or isnamedtuple(left)
    ):
        explanation = _compare_eq_cls(left, right)
    elif issequence(left) and issequence(right):
        explanation = _compare_eq_sequence(left, right)
    elif isset(left) and isset(right):
        explanation = _compare_eq_set(left, right)
    elif isdict(left) and isdict(right):
        explanation = _compare_eq_dict(left, right)


    if isiterable(left) and isiterable(right):
        expl = _compare_eq_iterable(left, right)
        explanation.extend(expl)

    return explanation


def _try_repr_or_str(obj: object) -> str:
    try:
        return repr(obj)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException:
        return f'{type(obj).__name__}("{obj}")'


def _format_repr_exception(exc: BaseException, obj: object) -> str:
    try:
        exc_info = _try_repr_or_str(exc)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:
        exc_info = f"unpresentable exception ({_try_repr_or_str(exc)})"
    return "<[{} raised in repr()] {} object at 0x{:x}>".format(
        exc_info, type(obj).__name__, id(obj)
    )


def _ellipsize(s: str, maxsize: int) -> str:
    """
    将字符串截断为指定的最大大小，使用省略号表示省略的部分。
    :param s:
    :param maxsize:
    :return:
    """
    if len(s) > maxsize:
        i = max(0, (maxsize - 3) // 2)
        j = max(0, maxsize - 3 - i)
        return s[:i] + "..." + s[len(s) - j :]
    return s


class SafeRepr(reprlib.Repr):
    """
    repr.Repr that limits the resulting size of repr() and includes
    information on exceptions raised during the call.
    """

    def __init__(self, maxsize: Optional[int], use_ascii: bool = False) -> None:
        """
        :param maxsize:
            If not None, will truncate the resulting repr to that specific size, using ellipsis
            somewhere in the middle to hide the extra text.
            If None, will not impose any size limits on the returning repr.
        """
        super().__init__()
        # ``maxstring`` is used by the superclass, and needs to be an int; using a
        # very large number in case maxsize is None, meaning we want to disable
        # truncation.
        self.maxstring = maxsize if maxsize is not None else 1_000_000_000
        self.maxsize = maxsize
        self.use_ascii = use_ascii

    def repr(self, x: object) -> str:
        try:
            if self.use_ascii:
                s = ascii(x)
            else:
                s = super().repr(x)

        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:
            s = _format_repr_exception(exc, x)
        if self.maxsize is not None:
            s = _ellipsize(s, self.maxsize)
        return s

    def repr_instance(self, x: object, level: int) -> str:
        try:
            s = repr(x)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:
            s = _format_repr_exception(exc, x)
        if self.maxsize is not None:
            s = _ellipsize(s, self.maxsize)
        return s




# Maximum size of overall repr of objects to display during assertion errors.
DEFAULT_REPR_MAX_SIZE = 240


def saferepr(
    obj: object, maxsize: Optional[int] = DEFAULT_REPR_MAX_SIZE, use_ascii: bool = False
) -> str:
    """Return a size-limited safe repr-string for the given object.

    Failing __repr__ functions of user instances will be represented
    with a short exception info and 'saferepr' generally takes
    care to never raise exceptions itself.

    This function is a wrapper around the Repr/reprlib functionality of the
    stdlib.
    """

    return SafeRepr(maxsize, use_ascii).repr(obj)





class AlwaysDispatchingPrettyPrinter(pprint.PrettyPrinter):
    """PrettyPrinter that always dispatches (regardless of width)."""

    def _format(
        self,
        object: object,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: Dict[int, Any],
        level: int,
    ) -> None:
        # Type ignored because _dispatch is private.
        p = self._dispatch.get(type(object).__repr__, None)  # type: ignore[attr-defined]

        objid = id(object)
        if objid in context or p is None:
            # Type ignored because _format is private.
            super()._format(  # type: ignore[misc]
                object,
                stream,
                indent,
                allowance,
                context,
                level,
            )
            return

        context[objid] = 1
        p(self, object, stream, indent, allowance, context, level + 1)
        del context[objid]


def _pformat_dispatch(
    object: object,
    indent: int = 1,
    width: int = 80,
    depth: Optional[int] = None,
    *,
    compact: bool = False,
) -> str:
    return AlwaysDispatchingPrettyPrinter(
        indent=indent, width=width, depth=depth, compact=compact
    ).pformat(object)






def _format_boolop(explanations: Iterable[str], is_or: bool) -> str:
    explanation = "(" + (is_or and " or " or " and ").join(explanations) + ")"
    return explanation.replace("%", "%%")





def format_explanation(explanation: str) -> str:
    r"""Format an explanation.

    Normally all embedded newlines are escaped, however there are
    three exceptions: \n{, \n} and \n~.  The first two are intended
    cover nested explanations, see function and attribute explanations
    for examples (.visit_Call(), visit_Attribute()).  The last one is
    for when one explanation needs to span multiple lines, e.g. when
    displaying diffs.
    """
    lines = _split_explanation(explanation)
    result = _format_lines(lines)
    return "\n".join(result)


def _split_explanation(explanation: str) -> List[str]:
    r"""Return a list of individual lines in the explanation.

    This will return a list of lines split on '\n{', '\n}' and '\n~'.
    Any other newlines will be escaped and appear in the line as the
    literal '\n' characters.
    """
    raw_lines = (explanation or "").split("\n")
    lines = [raw_lines[0]]
    for values in raw_lines[1:]:
        if values and values[0] in ["{", "}", "~", ">"]:
            lines.append(values)
        else:
            lines[-1] += "\\n" + values
    return lines


def _format_lines(lines: Sequence[str]) -> List[str]:
    """Format the individual lines.

    This will replace the '{', '}' and '~' characters of our mini formatting
    language with the proper 'where ...', 'and ...' and ' + ...' text, taking
    care of indentation along the way.

    Return a list of formatted lines.
    """
    result = list(lines[:1])
    stack = [0]
    stackcnt = [0]
    for line in lines[1:]:
        if line.startswith("{"):
            if stackcnt[-1]:
                s = "and   "
            else:
                s = "where "
            stack.append(len(result))
            stackcnt[-1] += 1
            stackcnt.append(0)
            result.append(" +" + "  " * (len(stack) - 1) + s + line[1:])
        elif line.startswith("}"):
            stack.pop()
            stackcnt.pop()
            result[stack[-1]] += line[1:]
        else:
            assert line[0] in ["~", ">"]
            stack[-1] += 1
            indent = len(stack) if line.startswith("~") else len(stack) - 1
            result.append("  " * indent + line[1:])
    assert len(stack) == 1
    return result


def issequence(x: Any) -> bool:
    return isinstance(x, collections.abc.Sequence) and not isinstance(x, str)


def istext(x: Any) -> bool:
    return isinstance(x, str)


def isdict(x: Any) -> bool:
    return isinstance(x, dict)


def isset(x: Any) -> bool:
    return isinstance(x, (set, frozenset))


def isnamedtuple(obj: Any) -> bool:
    return isinstance(obj, tuple) and getattr(obj, "_fields", None) is not None


def isdatacls(obj: Any) -> bool:
    return getattr(obj, "__dataclass_fields__", None) is not None


def isattrs(obj: Any) -> bool:
    return getattr(obj, "__attrs_attrs__", None) is not None


def isiterable(obj: Any) -> bool:
    try:
        iter(obj)
        return not istext(obj)
    except TypeError:
        return False


def has_default_eq(
    obj: object,
) -> bool:
    """Check if an instance of an object contains the default eq

    First, we check if the object's __eq__ attribute has __code__,
    if so, we check the equally of the method code filename (__code__.co_filename)
    to the default one generated by the dataclass and attr module
    for dataclasses the default co_filename is <string>, for attrs class, the __eq__ should contain "attrs eq generated"
    """
    # inspired from https://github.com/willmcgugan/rich/blob/07d51ffc1aee6f16bd2e5a25b4e82850fb9ed778/rich/pretty.py#L68
    if hasattr(obj.__eq__, "__code__") and hasattr(obj.__eq__.__code__, "co_filename"):
        code_filename = obj.__eq__.__code__.co_filename

        if isattrs(obj):
            return "attrs generated eq" in code_filename

        return code_filename == "<string>"  # data class
    return True





def compare_eq_any_explanation(left: Any, right: Any) -> List[str]:
    explanation = []
    if istext(left) and istext(right):
        explanation = _compare_eq_text(left,right)
    if type(left) == type(right) and (
        isdatacls(left) or isattrs(left) or isnamedtuple(left)
    ):
        explanation = _compare_eq_cls(left, right)
    elif issequence(left) and issequence(right):
        explanation = _compare_eq_sequence(left, right)
    elif isset(left) and isset(right):
        explanation = _compare_eq_set(left, right)
    elif isdict(left) and isdict(right):
        explanation = _compare_eq_dict(left, right)


    if isiterable(left) and isiterable(right):
        expl = _compare_eq_iterable(left, right)
        explanation.extend(expl)

    return explanation




def _surrounding_parens_on_own_lines(lines: List[str]) -> None:
    """Move opening/closing parenthesis/bracket to own lines."""
    opening = lines[0][:1]
    if opening in ["(", "[", "{"]:
        lines[0] = " " + lines[0][1:]
        lines[:] = [opening] + lines
    closing = lines[-1][-1:]
    if closing in [")", "]", "}"]:
        lines[-1] = lines[-1][:-1] + ","
        lines[:] = lines + [closing]


def _compare_eq_text(left:str,right:str)->List[str]:
    explanation = []
    differ = difflib.Differ()
    diff = differ.compare(left.splitlines(), right.splitlines())

    explanation.append("Detailed Text Comparison:")
    explanation.extend( line.rstrip() for line in diff)
    return explanation

def _compare_eq_iterable(
    left: Iterable[Any], right: Iterable[Any]
) -> List[str]:

    # dynamic import to speedup pytest
    import difflib

    left_formatting = pprint.pformat(left).splitlines()
    right_formatting = pprint.pformat(right).splitlines()

    # Re-format for different output lengths.
    lines_left = len(left_formatting)
    lines_right = len(right_formatting)
    if lines_left != lines_right:
        left_formatting = _pformat_dispatch(left).splitlines()

        right_formatting = _pformat_dispatch(right).splitlines()


    if lines_left > 1 or lines_right > 1:
        _surrounding_parens_on_own_lines(left_formatting)
        _surrounding_parens_on_own_lines(right_formatting)
    explanation = ["Full diff:"]
    # "right" is the expected base against which we compare "left",
    # see https://github.com/pytest-dev/pytest/issues/3333
    explanation.extend(
        line.rstrip() for line in difflib.ndiff(right_formatting, left_formatting)
    )
    return explanation


def _compare_eq_sequence(
    left: Sequence[Any], right: Sequence[Any]
) -> List[str]:
    comparing_bytes = isinstance(left, bytes) and isinstance(right, bytes)
    explanation: List[str] = []
    len_left = len(left)
    len_right = len(right)
    for i in range(min(len_left, len_right)):
        if left[i] != right[i]:
            if comparing_bytes:
                # when comparing bytes, we want to see their ascii representation
                # instead of their numeric values (#5260)
                # using a slice gives us the ascii representation:
                # >>> s = b'foo'
                # >>> s[0]
                # 102
                # >>> s[0:1]
                # b'f'
                left_value = left[i : i + 1]
                right_value = right[i : i + 1]
            else:
                left_value = left[i]
                right_value = right[i]

            explanation += [f"At index {i} diff: {left_value!r} != {right_value!r}"]
            break

    if comparing_bytes:
        # when comparing bytes, it doesn't help to show the "sides contain one or more
        # items" longer explanation, so skip it

        return explanation

    len_diff = len_left - len_right
    if len_diff:
        if len_diff > 0:
            dir_with_more = "Left"
            extra = saferepr(left[len_right])
        else:
            len_diff = 0 - len_diff
            dir_with_more = "Right"
            extra = saferepr(right[len_left])

        if len_diff == 1:
            explanation += [f"{dir_with_more} contains one more item: {extra}"]
        else:
            explanation += [
                "%s contains %d more items, first extra item: %s"
                % (dir_with_more, len_diff, extra)
            ]
    return explanation


def _compare_eq_set(
    left: AbstractSet[Any], right: AbstractSet[Any]
) -> List[str]:
    explanation = []
    diff_left = left - right
    diff_right = right - left
    if diff_left:
        explanation.append("Extra items in the left set:")
        for item in diff_left:
            explanation.append(saferepr(item))
    if diff_right:
        explanation.append("Extra items in the right set:")
        for item in diff_right:
            explanation.append(saferepr(item))
    return explanation


def _compare_eq_dict(
    left: Mapping[Any, Any], right: Mapping[Any, Any]
) -> List[str]:
    explanation: List[str] = []
    set_left = set(left)
    set_right = set(right)
    common = set_left.intersection(set_right)
    same = {k: left[k] for k in common if left[k] == right[k]}

    explanation += ["Common items:"]
    explanation += pprint.pformat(same).splitlines()

    diff = {k for k in common if left[k] != right[k]}
    if diff:
        explanation += ["Differing items:"]
        for k in diff:
            explanation += [saferepr({k: left[k]}) + " != " + saferepr({k: right[k]})]
    extra_left = set_left - set_right
    len_extra_left = len(extra_left)
    if len_extra_left:
        explanation.append(
            "Left contains %d more item%s:"
            % (len_extra_left, "" if len_extra_left == 1 else "s")
        )
        explanation.extend(
            pprint.pformat({k: left[k] for k in extra_left}).splitlines()
        )
    extra_right = set_right - set_left
    len_extra_right = len(extra_right)
    if len_extra_right:
        explanation.append(
            "Right contains %d more item%s:"
            % (len_extra_right, "" if len_extra_right == 1 else "s")
        )
        explanation.extend(
            pprint.pformat({k: right[k] for k in extra_right}).splitlines()
        )
    return explanation


def _compare_eq_cls(left: Any, right: Any) -> List[str]:
    if not has_default_eq(left):
        return []
    if isdatacls(left):
        import dataclasses

        all_fields = dataclasses.fields(left)
        fields_to_check = [info.name for info in all_fields if info.compare]
    elif isattrs(left):
        all_fields = left.__attrs_attrs__
        fields_to_check = [field.name for field in all_fields if getattr(field, "eq")]
    elif isnamedtuple(left):
        fields_to_check = left._fields
    else:
        assert False

    indent = "  "
    same = []
    diff = []
    for field in fields_to_check:
        if getattr(left, field) == getattr(right, field):
            same.append(field)
        else:
            diff.append(field)

    explanation = []

    explanation += ["Matching attributes:"]
    explanation += pprint.pformat(same).splitlines()
    if diff:
        explanation += ["Differing attributes:"]
        explanation += pprint.pformat(diff).splitlines()
        for field in diff:
            field_left = getattr(left, field)
            field_right = getattr(right, field)
            explanation += [
                "",
                "Drill down into differing attribute %s:" % field,
                ("%s%s: %r != %r") % (indent, field, field_left, field_right),
            ]
            explanation += [
                indent + line
                for line in _compare_eq_any(field_left, field_right)
            ]
    return explanation




# bytes1 = bytearray([0x01,0x02])
# bytes2 = bytearray([0x02,0x02])
# print("\n".join(_compare_eq_any(bytes1,bytes2)))
#
# print("\n".join(_compare_eq_any("A B","A D")))
#
# text1 = "HAD EF."
# text2 = "GA FFD"
#
# print("\n".join(_compare_eq_any(text1,text2)))





# # Compare text values
# explanation = _diff_text("Hello", "World", verbose=1)
# print("Compare text values:")
# print('\n'.join(explanation))
