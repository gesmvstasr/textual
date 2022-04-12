import pytest


from textual.color import Color
from textual.css.errors import UnresolvedVariableError
from textual.css.parse import substitute_references
from textual.css.scalar import Scalar, Unit
from textual.css.stylesheet import Stylesheet, StylesheetParseError
from textual.css.tokenize import tokenize
from textual.css.tokenizer import Token, ReferencedBy
from textual.css.transition import Transition
from textual.geometry import Spacing
from textual.layouts.dock import DockLayout


class TestVariableReferenceSubstitution:
    def test_simple_reference(self):
        css = "$x: 1; #some-widget{border: $x;}"
        variables = substitute_references(tokenize(css, ""))
        assert list(variables) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value=";",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 6),
                referenced_by=None,
            ),
            Token(
                name="selector_start_id",
                value="#some-widget",
                path="",
                code=css,
                location=(0, 7),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(0, 19),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(0, 20),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 27),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="x", location=(0, 28), length=2),
            ),
            Token(
                name="declaration_end",
                value=";",
                path="",
                code=css,
                location=(0, 30),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(0, 31),
                referenced_by=None,
            ),
        ]

    def test_simple_reference_no_whitespace(self):
        css = "$x:1; #some-widget{border: $x;}"
        variables = substitute_references(tokenize(css, ""))
        assert list(variables) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value=";",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=None,
            ),
            Token(
                name="selector_start_id",
                value="#some-widget",
                path="",
                code=css,
                location=(0, 6),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(0, 18),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(0, 19),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 26),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=ReferencedBy(name="x", location=(0, 27), length=2),
            ),
            Token(
                name="declaration_end",
                value=";",
                path="",
                code=css,
                location=(0, 29),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(0, 30),
                referenced_by=None,
            ),
        ]

    def test_undefined_variable(self):
        css = ".thing { border: $not-defined; }"
        with pytest.raises(UnresolvedVariableError):
            list(substitute_references(tokenize(css, "")))

    def test_transitive_reference(self):
        css = "$x: 1\n$y: $x\n.thing { border: $y }"
        assert list(substitute_references(tokenize(css, ""))) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value="\n",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=None,
            ),
            Token(
                name="variable_name",
                value="$y:",
                path="",
                code=css,
                location=(1, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="x", location=(1, 4), length=2),
            ),
            Token(
                name="variable_value_end",
                value="\n",
                path="",
                code=css,
                location=(1, 6),
                referenced_by=None,
            ),
            Token(
                name="selector_start_class",
                value=".thing",
                path="",
                code=css,
                location=(2, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 6),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(2, 7),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 8),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(2, 9),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 16),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 19),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(2, 20),
                referenced_by=None,
            ),
        ]

    def test_multi_value_variable(self):
        css = "$x: 2 4\n$y: 6 $x 2\n.thing { border: $y }"
        assert list(substitute_references(tokenize(css, ""))) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="2",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="4",
                path="",
                code=css,
                location=(0, 6),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value="\n",
                path="",
                code=css,
                location=(0, 7),
                referenced_by=None,
            ),
            Token(
                name="variable_name",
                value="$y:",
                path="",
                code=css,
                location=(1, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="6",
                path="",
                code=css,
                location=(1, 4),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 5),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="2",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="x", location=(1, 6), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=ReferencedBy(name="x", location=(1, 6), length=2),
            ),
            Token(
                name="number",
                value="4",
                path="",
                code=css,
                location=(0, 6),
                referenced_by=ReferencedBy(name="x", location=(1, 6), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 8),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="2",
                path="",
                code=css,
                location=(1, 9),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value="\n",
                path="",
                code=css,
                location=(1, 10),
                referenced_by=None,
            ),
            Token(
                name="selector_start_class",
                value=".thing",
                path="",
                code=css,
                location=(2, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 6),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(2, 7),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 8),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(2, 9),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 16),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="6",
                path="",
                code=css,
                location=(1, 4),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 5),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="number",
                value="2",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 5),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="number",
                value="4",
                path="",
                code=css,
                location=(0, 6),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 8),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="number",
                value="2",
                path="",
                code=css,
                location=(1, 9),
                referenced_by=ReferencedBy(name="y", location=(2, 17), length=2),
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(2, 19),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(2, 20),
                referenced_by=None,
            ),
        ]

    def test_variable_used_inside_property_value(self):
        css = "$x: red\n.thing { border: on $x; }"
        assert list(substitute_references(tokenize(css, ""))) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="token",
                value="red",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value="\n",
                path="",
                code=css,
                location=(0, 7),
                referenced_by=None,
            ),
            Token(
                name="selector_start_class",
                value=".thing",
                path="",
                code=css,
                location=(1, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 6),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(1, 7),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 8),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(1, 9),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 16),
                referenced_by=None,
            ),
            Token(
                name="token",
                value="on",
                path="",
                code=css,
                location=(1, 17),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 19),
                referenced_by=None,
            ),
            Token(
                name="token",
                value="red",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=ReferencedBy(name="x", location=(1, 20), length=2),
            ),
            Token(
                name="declaration_end",
                value=";",
                path="",
                code=css,
                location=(1, 22),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(1, 23),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(1, 24),
                referenced_by=None,
            ),
        ]

    def test_variable_definition_eof(self):
        css = "$x: 1"
        assert list(substitute_references(tokenize(css, ""))) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="1",
                path="",
                code=css,
                location=(0, 4),
                referenced_by=None,
            ),
        ]

    def test_variable_reference_whitespace_trimming(self):
        css = "$x:    123;.thing{border: $x}"
        assert list(substitute_references(tokenize(css, ""))) == [
            Token(
                name="variable_name",
                value="$x:",
                path="",
                code=css,
                location=(0, 0),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value="    ",
                path="",
                code=css,
                location=(0, 3),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="123",
                path="",
                code=css,
                location=(0, 7),
                referenced_by=None,
            ),
            Token(
                name="variable_value_end",
                value=";",
                path="",
                code=css,
                location=(0, 10),
                referenced_by=None,
            ),
            Token(
                name="selector_start_class",
                value=".thing",
                path="",
                code=css,
                location=(0, 11),
                referenced_by=None,
            ),
            Token(
                name="declaration_set_start",
                value="{",
                path="",
                code=css,
                location=(0, 17),
                referenced_by=None,
            ),
            Token(
                name="declaration_name",
                value="border:",
                path="",
                code=css,
                location=(0, 18),
                referenced_by=None,
            ),
            Token(
                name="whitespace",
                value=" ",
                path="",
                code=css,
                location=(0, 25),
                referenced_by=None,
            ),
            Token(
                name="number",
                value="123",
                path="",
                code=css,
                location=(0, 7),
                referenced_by=ReferencedBy(name="x", location=(0, 26), length=2),
            ),
            Token(
                name="declaration_set_end",
                value="}",
                path="",
                code=css,
                location=(0, 28),
                referenced_by=None,
            ),
        ]


class TestParseLayout:
    def test_valid_layout_name(self):
        css = "#some-widget { layout: dock; }"

        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles
        assert isinstance(styles.layout, DockLayout)

    def test_invalid_layout_name(self):
        css = "#some-widget { layout: invalidlayout; }"

        stylesheet = Stylesheet()
        with pytest.raises(StylesheetParseError) as ex:
            stylesheet.parse(css)

        assert ex.value.errors is not None


class TestParseText:
    def test_foreground(self):
        css = """#some-widget {
            color: green;
        }
        """
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles
        assert styles.color == Color.parse("green")

    def test_background(self):
        css = """#some-widget {
            background: red;
        }
        """
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles
        assert styles.background == Color.parse("red")


class TestParseOffset:
    @pytest.mark.parametrize(
        "offset_x, parsed_x, offset_y, parsed_y",
        [
            [
                "-5.5%",
                Scalar(-5.5, Unit.PERCENT, Unit.WIDTH),
                "-30%",
                Scalar(-30, Unit.PERCENT, Unit.HEIGHT),
            ],
            [
                "5%",
                Scalar(5, Unit.PERCENT, Unit.WIDTH),
                "40%",
                Scalar(40, Unit.PERCENT, Unit.HEIGHT),
            ],
            [
                "10",
                Scalar(10, Unit.CELLS, Unit.WIDTH),
                "40",
                Scalar(40, Unit.CELLS, Unit.HEIGHT),
            ],
        ],
    )
    def test_composite_rule(self, offset_x, parsed_x, offset_y, parsed_y):
        css = f"""#some-widget {{
            offset: {offset_x} {offset_y};
        }}
        """
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles

        assert len(stylesheet.rules) == 1
        assert stylesheet.rules[0].errors == []
        assert styles.offset.x == parsed_x
        assert styles.offset.y == parsed_y

    @pytest.mark.parametrize(
        "offset_x, parsed_x, offset_y, parsed_y",
        [
            [
                "-5.5%",
                Scalar(-5.5, Unit.PERCENT, Unit.WIDTH),
                "-30%",
                Scalar(-30, Unit.PERCENT, Unit.HEIGHT),
            ],
            [
                "5%",
                Scalar(5, Unit.PERCENT, Unit.WIDTH),
                "40%",
                Scalar(40, Unit.PERCENT, Unit.HEIGHT),
            ],
            [
                "-10",
                Scalar(-10, Unit.CELLS, Unit.WIDTH),
                "40",
                Scalar(40, Unit.CELLS, Unit.HEIGHT),
            ],
        ],
    )
    def test_separate_rules(self, offset_x, parsed_x, offset_y, parsed_y):
        css = f"""#some-widget {{
            offset-x: {offset_x};
            offset-y: {offset_y};
        }}
        """
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles

        assert len(stylesheet.rules) == 1
        assert stylesheet.rules[0].errors == []
        assert styles.offset.x == parsed_x
        assert styles.offset.y == parsed_y


class TestParseTransition:
    @pytest.mark.parametrize(
        "duration, parsed_duration",
        [
            ["5.57s", 5.57],
            ["0.5s", 0.5],
            ["1200ms", 1.2],
            ["0.5ms", 0.0005],
            ["20", 20.0],
            ["0.1", 0.1],
        ],
    )
    def test_various_duration_formats(self, duration, parsed_duration):
        easing = "in_out_cubic"
        transition_property = "offset"
        css = f"""#some-widget {{
            transition: {transition_property} {duration} {easing} {duration};
        }}
        """
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles

        assert len(stylesheet.rules) == 1
        assert stylesheet.rules[0].errors == []
        assert styles.transitions == {
            "offset": Transition(
                duration=parsed_duration, easing=easing, delay=parsed_duration
            )
        }

    def test_no_delay_specified(self):
        css = f"#some-widget {{ transition: offset-x 1 in_out_cubic; }}"
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        styles = stylesheet.rules[0].styles

        assert stylesheet.rules[0].errors == []
        assert styles.transitions == {
            "offset-x": Transition(duration=1, easing="in_out_cubic", delay=0)
        }

    def test_unknown_easing_function(self):
        invalid_func_name = "invalid_easing_function"
        css = f"#some-widget {{ transition: offset 1 {invalid_func_name} 1; }}"

        stylesheet = Stylesheet()
        with pytest.raises(StylesheetParseError) as ex:
            stylesheet.parse(css)

        stylesheet_errors = stylesheet.rules[0].errors

        assert len(stylesheet_errors) == 1
        assert stylesheet_errors[0][0].value == invalid_func_name
        assert ex.value.errors is not None


class TestParseOpacity:
    @pytest.mark.parametrize(
        "css_value, styles_value",
        [
            ["-0.2", 0.0],
            ["0.4", 0.4],
            ["1.3", 1.0],
            ["-20%", 0.0],
            ["25%", 0.25],
            ["128%", 1.0],
        ],
    )
    def test_opacity_to_styles(self, css_value, styles_value):
        css = f"#some-widget {{ opacity: {css_value} }}"
        stylesheet = Stylesheet()
        stylesheet.parse(css)

        assert stylesheet.rules[0].styles.opacity == styles_value
        assert not stylesheet.rules[0].errors

    def test_opacity_invalid_value(self):
        css = "#some-widget { opacity: 123x }"
        stylesheet = Stylesheet()

        with pytest.raises(StylesheetParseError):
            stylesheet.parse(css)
        assert stylesheet.rules[0].errors


class TestParseMargin:
    def test_margin_partial(self):
        css = "#foo {margin: 1; margin-top: 2; margin-right: 3; margin-bottom: -1;}"
        stylesheet = Stylesheet()
        stylesheet.parse(css)
        assert stylesheet.rules[0].styles.margin == Spacing(2, 3, -1, 1)


class TestParsePadding:
    def test_padding_partial(self):
        css = "#foo {padding: 1; padding-top: 2; padding-right: 3; padding-bottom: -1;}"
        stylesheet = Stylesheet()
        stylesheet.parse(css)
        assert stylesheet.rules[0].styles.padding == Spacing(2, 3, -1, 1)
