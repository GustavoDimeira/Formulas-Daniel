from js import console, document
import sympy as sp

variables = sp.symbols('a b c d e f g h')

div = document.getElementById("variables_inputs")

for var in variables:
  div.innerHTML += """
<label id="var-{}>
  <p">{}<p/>
  <input/>
</label>
      """.format(var, var)


def calculate():
    elements = document.querySelectorAll("#variables_inputs input")

    counter = 0
    a, b, c, d, e, f, g, h = variables

    for element in elements:
      try:
        value = element.value
        value_as_sympy = sp.sympify(value)
        if(counter == 0): a = value_as_sympy
        if(counter == 1): b = value_as_sympy
        if(counter == 2): c = value_as_sympy
        if(counter == 3): d = value_as_sympy
        if(counter == 4): e = value_as_sympy
        if(counter == 5): f = value_as_sympy
        if(counter == 6): g = value_as_sympy
        if(counter == 7): h = value_as_sympy
      except sp.SympifyError:
        pass
      except ValueError:
        pass
      counter += 1

    equation = [
      sp.Eq(a + b, c),
      sp.Eq((c+1) * d, b),
      sp.Eq(((a*c + 15*b) / 2), e),
      sp.Eq(f + c * a, e),
      sp.Eq(a ** 2 + 32 * f - b ** 2, g),
      sp.Eq(a + b + c + d + e + f + g + h, 0)
    ]

    values = sp.solve(equation, variables)
    
    quoted_vars = ['{}'.format(val) for val in variables]
    quoted_sol = ['"{}"'.format(val) for val in values[0]]

    listOfValues = []

    for i in range(len(quoted_vars)):
        listOfValues.append('\n    ' + quoted_vars[i] + ': ' + quoted_sol[i])

    content = """
  values: {}
    """.format(
        '{' + ','.join(listOfValues) + '\n  }',
    )

    print(content)
    print(a)
