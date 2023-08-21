import sympy as sp

variables = sp.symbols('a b c d e f g h')
a, b, c, d, e, f, g, h = variables

a = 5
b = 10

equation = [
    sp.Eq(a + b, c),
    sp.Eq((c+1) * d, b),
    sp.Eq(((a*c + 15*b) / 2), e),
    sp.Eq(f + c * a, e),
    sp.Eq(a ** 2 + 32 * f - b ** 2, g)
]

solution = sp.solve(equation, variables)

quoted_vars = ['"{}"'.format(val) for val in variables]
quoted_sol = ['"{}"'.format(val) for val in solution[0]]

listOfValues = []

for i in range(len(quoted_vars)):
    listOfValues.append('\n    ' + quoted_vars[i] + ': ' + quoted_sol[i])

content = """{{
"values": {}
}}""".format(
    '{' + ','.join(listOfValues) + '\n  }',
)

print(content)
