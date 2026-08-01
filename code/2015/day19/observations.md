- String has a formal grammar which could be parsed (i.e. with Lark)

- Collapse input -> `e` (instead of the other way around)
- Leverage "output"-only elements (i.e. `Rn`, `Ar`, `Y`, `C`), which are never used as inputs
- Consider potentially constructing the string from left-to-right, which could anchor some subsections
- Lowercase chars never appear on their own (always with a capital character as part of an element)

- Any substitution which produces at least one "output"-only char will always produce a string in the form: `..Rn..Ar..` (Variations include `..Rn..Y..Ar` and `..Rn..Y..Y..Ar`)
    - So `..Rn..Ar` can be used as a general constraint. Innermost Rn-Ar pairings behave much like '(' and ')'

- The innermost Rn-Ar regions (the `..` in `Rn..Ar`) only ever contain ONE element
- No replacement ever adds an element after `Ar`; `Ar` is always the last element in the output (if present)
- No output containing `Rn` ever starts with `Rn` (it is always prefixed by ONE other character)
