from dataclasses import dataclass, field, fields


@dataclass
class Attribute:
    """ Атрибут """
    name: str = ""
    value: str = ""


@dataclass
class Option:
    """ Параметр """
    name: str = ""
    left: str = ""
    right: str = ""
    unit_measure: str = ""
    step: str = ""
    option_type: str = ""


@dataclass
class Quote:
    """ Расценка """
    table: str = ""
    code: str = ""
    title: str = ""
    measure: str = ""
    type_quote: str = ""
    parent_quote: str = ""
    attributes: list[Attribute] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)
