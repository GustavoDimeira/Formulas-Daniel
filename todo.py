from js import document
import sympy as sp

meters_to_inches = 0.0254 ** -1
inches_to_milimeters = 25.4

variables_g_1 = sp.symbols("Pcᵍ Pbᵍ Pdᵍ Nᵍ dᵍ mᵍ")
variables_p_1 = sp.symbols("Pcᵖ Pbᵖ Pdᵖ Nᵖ dᵖ mᵖ")

variables_g_2 = sp.symbols("Fᵍ Jᵍ Qvᵍ Vtᵍ trᵍ rpmᵍ potᵍ")
variables_p_2 = sp.symbols("Fᵖ Jᵖ Qvᵖ Vtᵖ trᵖ rpmᵖ potᵖ")

variables_g_3 = sp.symbols("Tᵍ N_cicleᵍ Sfb_linha_ᵍ")
variables_p_3 = sp.symbols("Tᵖ N_cicleᵖ Sfb_linha_ᵖ")

gear_teeth = {}
pinion_teeth = {}

def render_inputs(container, names, metric_units):
    container.innerHTML = ''
    for i in range(len(names)):
        container.innerHTML += """
<label id="var-{}">
  <p>{}</p>
  <input>
  <p>{}</p>
</label>
""".format(names[i], names[i], metric_units[i])


def first_inputs():
    metric_units = ['in', 'in', 'in-¹', 'variavel', 'metros', 'milimetros']

    gear = document.querySelector("#first_section .gear")
    pinion = document.querySelector("#first_section .pinion")

    render_inputs(gear, variables_g_1, metric_units)
    render_inputs(pinion, variables_p_1, metric_units)


first_inputs()

def calc_first():
    elements = document.querySelectorAll("#first_section input")
    counter = 0
    θ = document.querySelector("#angle").value

    Pcᵍ, Pbᵍ, Pdᵍ, Nᵍ, dᵍ, mᵍ = variables_g_1
    Pcᵖ, Pbᵖ, Pdᵖ, Nᵖ, dᵖ, mᵖ = variables_p_1

    for element in elements:
        try:
            value_as_sympy = sp.sympify(element.value)
            if (counter == 0): Pcᵍ = value_as_sympy
            if (counter == 1): Pbᵍ = value_as_sympy
            if (counter == 2): Pdᵍ = value_as_sympy
            if (counter == 3): Nᵍ = value_as_sympy
            if (counter == 4): dᵍ = value_as_sympy * meters_to_inches
            if (counter == 5): mᵍ = value_as_sympy
            if (counter == 6): Pcᵖ = value_as_sympy
            if (counter == 7): Pbᵖ = value_as_sympy
            if (counter == 8): Pdᵖ = value_as_sympy
            if (counter == 9): Nᵖ = value_as_sympy
            if (counter == 10): dᵖ = value_as_sympy * meters_to_inches
            if (counter == 11): mᵖ = value_as_sympy
        except sp.SympifyError:
            pass
        counter += 1

    equations = [
        sp.Eq(Pcg, sp.pi * dg / Ng),
        sp.Eq(Pbg, Pcg * sp.cos(θ)),
        sp.Eq(Pdg, Ng / dg),
        sp.Eq(mg, (dg * inches_to_milimeters) / Ng),
        sp.Eq(Pcp, sp.pi * dp / Np),
        sp.Eq(Pbp, Pcp * sp.cos(θ)),
        sp.Eq(Pdp, Np / dp),
        sp.Eq(mp, (dp * inches_to_milimeters) / Np),
    ]

    solution = sp.solve(equations, variables_g_1 + variables_p_1)

    Pdᵍ_value = solution[Pdᵍ]
    Pdᵖ_value = solution[Pdᵖ]

    gear_teeth = {
        "adendo": [1/Pdᵍ_value, "in-¹"],
        "dedendo": [1.25/Pdᵍ_value, "in-¹"],
        "profundidade de trabalo": [2/Pdᵍ_value, "in-¹"],
        "profundidade total": [2.25/Pdᵍ_value if (1 < 20) else ((2.2/Pdᵍ_value) + 0.002), "in-¹"],
        "espessura circular dente": [1.571/Pdᵍ_value, "in-¹"],
        "raio arredondamento": [0.3/Pdᵍ_value if (1 < 20) else "não padronizado", "in-¹"],
        "folga basica minima": [0.25/Pdᵍ_value if (1 < 20) else ((0.2/Pdᵍ_value) + 0.002), "in-¹"],
        "largura minima topo": [0.25/Pdᵍ_value if (1 < 20) else "não padronizado", "in-¹"],
        "folga dentes polidos": [0.35/Pdᵍ_value if (1 < 20) else ((0.35/Pdᵍ_value) + 0.002), "in-¹"],
    }

    pinion_teeth = {
        "adendo": [1/Pdᵖ_value, "in-¹"],
        "dedendo": [1.25/Pdᵖ_value, "in-¹"],
        "profundidade de trabalo": [2/Pdᵖ_value, "in-¹"],
        "profundidade total": [2.25/Pdᵖ_value if (1 < 20) else ((2.2/Pdᵖ_value) + 0.002), "in-¹"],
        "espessura circular dente": [1.571/Pdᵖ_value, "in-¹"],
        "raio arredondamento": [0.3/Pdᵖ_value if (1 < 20) else "não padronizado", "in-¹"],
        "folga basica minima": [0.25/Pdᵖ_value if (1 < 20) else ((0.2/Pdᵖ_value) + 0.002), "in-¹"],
        "largura minima topo": [0.25/Pdᵖ_value if (1 < 20) else "não padronizado", "in-¹"],
        "folga dentes polidos": [0.35/Pdᵖ_value if (1 < 20) else ((0.35/Pdᵖ_value) + 0.002), "in-¹"],
    }

    variables_Z_1 = sp.symbols('ra_p rcos_p ra_g rcos_g C z')
    ra_p, rcos_p, ra_g, rcos_g, c, z = variables_Z_1

    try:
        d_p = solution[dᵖ]
    except KeyError:
        d_p = dᵖ

    try:
        d_g = solution[dᵍ]
    except KeyError:
        d_g = dᵍ

    ra_p = (d_p / 2 + pinion_teeth["adendo"][0]) ** 2
    rcos_p = ((d_p / 2) * sp.cos(θ)) ** 2
    ra_g = (d_g / 2 + gear_teeth["adendo"][0]) ** 2
    rcos_g = ((d_g / 2) * sp.cos(θ)) ** 2

    c = d_g / 2 + d_p / 2

    solution_z = sp.solve(
        sp.Eq(((ra_p - rcos_p) ** (1/2)) +
              ((ra_g - rcos_g) ** (1/2)) - (c * sp.sin(θ)), z),
        variables_Z_1
    )

    mpᵍ = abs(solution_z[0][-1] / solution[Pbᵍ])
    mpᵖ = abs(solution_z[0][-1] / solution[Pbᵖ])

    show_values(gear_teeth, pinion_teeth, mpᵍ, mpᵖ, solution, c)


def show_values(gear_teeth, pinion_teeth, mpᵍ, mpᵖ, solution, c):
    div = document.querySelector("#first_section .calculated_values")

    div.innerHTML = """
<div id="inputs_solution">
  <h3>Solução dos campos de input</h3>
  <section>  
    <table class="booth"> 
      <tr>
        <th>Nome</th>
        <th>Valor</th>
      </tr>
      <tb/>
    </table>
  </section>
</div>
<div id="table_values">
  <h3>Valores calculados a partir da tabela</h3>
  <section>
    <table class="gear">
      <tr>
        <th>Nome</th>
        <th>Valor</th>
        <th>Unidade</th>
      </tr>
      <tb/>
    </table>
    <table class="pinion">
      <tr>
        <th>Nome</th>
        <th>Valor</th>
        <th>Unidade</th>
      </tr>
      <tb/>
    </table>
  </section>
</div>
<section id=z_values>
  <h3>Outros Prametros</h3>
  <div>
    <h4>N° dentes em contato</h4>
    <span>Gear: {}</span>
    <span>Pinion: {}</span>
    <h4>Distancia entre centros:</h4>
    <span id="centers">{}</span>
  </div>
</section>
""".format(round(float(mpᵍ), 4), round(float(mpᵖ), 4), round(c, 4))

    input_solutions = document.querySelector("#inputs_solution tbody")
    for key, value in solution.items():
        input_solutions.innerHTML += """
  <tr id="row-{}">
    <td>{}</td>
    <td>{}</td>
  </tr>
""".format(key, key, round(value, 2))

    gear_table_solutions = document.querySelector("#table_values .gear tbody")
    for key, value in gear_teeth.items():
        gear_table_solutions.innerHTML += """
      <tr id="row-{}">
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
""".format(key, key, round(value[0], 2), value[1])

    pinion_table_solutions = document.querySelector("#table_values .pinion tbody")
    for key, value in pinion_teeth.items():
        pinion_table_solutions.innerHTML += """
      <tr id="row-{}">
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
""".format(key, key, round(value[0], 2), value[1])
    second_inputs()


def second_inputs():
    metric_units = ['in', 'variavel', 'variavel', 'm/s', 'in', 'variavel', '', '']

    gear = document.querySelector("#second_section .gear")
    pinion = document.querySelector("#second_section .pinion")
    extra =  document.querySelector("#second_section .extra")

    render_inputs(gear, variables_g_2, metric_units)
    render_inputs(pinion, variables_p_2, metric_units)

    gear.innerHTML += """
<div id=gear-select>
  <label>
    <span>Maquina Motora</span>
    <select class="motor">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="2">Choque medio</option>
    </select>
  </label>
  <label>
    <span>Maquina Movida</span>
    <select class="moveable">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="3">Choque medio</option>
    </select>
  </label>
</div>
<label>
  <span>Ksᵍ</span>
  <select id="var-Ksᵍ">
    <option value="1">1</option>
    <option value="1.25">1.25</option>
    <option value="1.5">1.5</option>
  </select>
</label>
"""

    pinion.innerHTML += """
<div id=pinion-select>
  <label>
    <span>Maquina Motora</span>
    <select class="motor">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="2">Choque medio</option>
    </select>
  </label>
  <label>
    <span>Maquina Movida</span>
    <select class="moveable">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="3">Choque medio</option>
    </select>
  </label>
</div>
<label>
  <span>Ksᵖ</span>
  <select id="var-Ksᵖ">
    <option value="1">1</option>
    <option value="1.25">1.25</option>
    <option value="1.5">1.5</option>
  </select>
</label>
"""

    extra.innerHTML = """
<label>
  <span>Ksᵖ</span>
  <select id="var-Ksᵖ">
    <option value="1">1</option>
    <option value="1.25">1.25</option>
    <option value="1.5">1.5</option>
  </select>
</label>
<label>
  <span>Material 1</span>
  <select id="material_1">
    <option value = 0>Aço</option>
    <option value = 1>Ferro maleavel</option>
    <option value = 2>Ferro nodular</option>
    <option value = 3>Ferro fundido</option>
    <option value = 4>Alumínio bronze</option>
    <option value = 5>Estanho bronze</option>
  </select>
</label>
<label>
  <span>Material 2</span>
  <select id="material_2">
    <option value = 0>Aço</option>
    <option value = 1>Ferro maleavel</option>
    <option value = 2>Ferro nodular</option>
    <option value = 3>Ferro fundido</option>
    <option value = 4>Alumínio bronze</option>
    <option value = 5>Estanho bronze</option>
  </select>
</label>
<label>
  <span>Posição dos Dentes</span>
  <select id="teeth_position">
    <option value = 1>Externo</option>
    <option value = -1>Interno</option>
  </select>
</label>
"""


def calc_second():
    try:
        elements = document.querySelectorAll("#second_section input")
        counter = 0

        value_g = document.querySelector("#var-mᵍ input").value
        value_p = document.querySelector("#var-mᵖ input").value

        mg = float(value_g) if (value_g) else float(document.querySelectorAll("#row-mᵍ td")[1].innerHTML)
        mp = float(value_p) if (value_p) else float(document.querySelectorAll("#row-mᵖ td")[1].innerHTML)

        Fᵍ, Jᵍ, Qvᵍ, Vtᵍ, trᵍ, rpmᵍ, potᵍ = variables_g_2
        Fᵖ, Jᵖ, Qvᵖ, Vtᵖ, trᵖ, rpmᵖ, potᵖ = variables_p_2

        for element in elements:
        
            value_as_sympy = sp.sympify(element.value)
            if (counter == 0): Fᵍ = value_as_sympy
            if (counter == 1): Jᵍ = value_as_sympy
            if (counter == 2): Qvᵍ = value_as_sympy
            if (counter == 3): Vtᵍ = value_as_sympy
            if (counter == 4): trᵍ = value_as_sympy
            if (counter == 5): rpmᵍ = value_as_sympy
            if (counter == 6): potᵍ = value_as_sympy
            if (counter == 7): Fᵖ = value_as_sympy
            if (counter == 8): Jᵖ = value_as_sympy
            if (counter == 9): Qvᵖ = value_as_sympy
            if (counter == 10): Vtᵖ = value_as_sympy
            if (counter == 11): trᵖ = value_as_sympy
            if (counter == 12): rpmᵖ = value_as_sympy
            if (counter == 13): potᵖ = value_as_sympy
            counter += 1

        if ((Fᵍ / 8) > mᵍ): Fᵍ = 8 * mᵍ
        if ((Fᵍ / 16) < mᵍ): Fᵍ = 16 * mᵍ

        if ((Fᵖ / 8) > mᵖ): Fᵖ = 8 * mᵖ
        if ((Fᵖ / 16) < mᵖ): Fᵖ = 16 * mᵖ

        Qvᵍ_fpm = Qvᵍ * 196.850394
        Qvᵖ_fpm = Qvᵖ * 196.850394

        if (Vtᵍ > 0 and Vtᵍ <= 800):
            if (not Qvᵍ_fpm > 6 or not Qvᵍ_fpm < 8): Qvᵍ = 7
        if (Vtᵍ > 800 and Vtᵍ <= 2000):
            if (not Qvᵍ_fpm > 8 or not Qvᵍ_fpm < 10): Qvᵍ = 9
        if (Vtᵍ > 2000 and Vtᵍ <= 4000):
            if (not Qvᵍ_fpm > 10 or not Qvᵍ_fpm < 12): Qvᵍ = 11
        if (Vtᵍ > 4000):
            if (not Qvᵍ_fpm > 12 or not Qvᵍ_fpm < 14): Qvᵍ = 13

        if (Vtᵖ > 0 and Vtᵖ <= 800):
            if (not Qvᵖ_fpm > 6 or not Qvᵖ_fpm < 8): Qvᵖ = 7
        if (Vtᵖ > 800 and Vtᵖ <= 2000):
            if (not Qvᵖ_fpm > 8 or not Qvᵖ_fpm < 10): Qvᵖ = 9
        if (Vtᵖ > 2000 and Vtᵖ <= 4000):
            if (not Qvᵖ_fpm > 10 or not Qvᵖ_fpm < 12): Qvᵖ = 11
        if (Vtᵖ > 4000):
            if (not Qvᵖ_fpm > 12 or not Qvᵖ_fpm < 14): Qvᵖ = 13

        Bᵍ = ((12 / Qvᵍ) ** (2/3)) / 4
        Aᵍ = 50 + 56 * (1 - Bᵍ)
        val_1ᵍ = document.querySelector("#gear-select .motor").value
        val_2ᵍ = document.querySelector("#gear-select .moveable").value
        adendo_g = float(document.querySelectorAll("#table_values .gear #row-adendo td")[1].innerHTML) 
        dedendo_g = float(document.querySelectorAll("#table_values .gear #row-dedendo td")[1].innerHTML)
        mbᵍ = trᵍ / (adendo_g + dedendo_g)

        Bᵖ = ((12 / Qvᵖ) ** (2/3)) / 4
        Aᵖ = 50 + 56 * (1 - Bᵖ)
        val_1ᵖ = document.querySelector("#pinion-select .motor").value
        val_2ᵖ = document.querySelector("#pinion-select .moveable").value
        adendo_p = float(document.querySelectorAll("#table_values .pinion #row-adendo td")[1].innerHTML)
        dedendo_p = float(document.querySelectorAll("#table_values .pinion #row-dedendo td")[1].innerHTML)
        mbᵖ = trᵖ / (adendo_p + dedendo_p)

        kvᵍ = (Aᵍ / (Aᵍ + ((200 * Vtᵍ) ** 1/2))) ** Bᵍ
        Kaᵍ = 1 + ((int(val_1ᵍ) + int(val_2ᵍ)) * 0.25)
        Kbᵍ = -2 * mbᵍ + 3.4 if (mbᵍ >= 0.5 and mbᵍ <= 1.2) else 1
        Ksᵍ = float(document.querySelector("#var-Ksᵍ").value)
        Kiᵍ = 1
        
        if Fᵍ < 50: kmᵍ = 1.6
        if Fᵍ < 150: kmᵍ = 1.7
        if Fᵍ < 250: kmᵍ = 1.8
        if Fᵍ < 500: kmᵍ = 1.9
        if Fᵍ >= 500: kmᵍ = 2

        kvᵖ = (Aᵖ / (Aᵖ + ((200 * Vtᵖ) ** 1/2))) ** Bᵖ
        Kaᵖ = 1 + ((int(val_1ᵖ) + int(val_2ᵖ)) * 0.25)
        Kbᵖ = -2 * mbᵖ + 3.4 if (mbᵖ >= 0.5 and mbᵖ <= 1.2) else 1
        Ksᵖ = float(document.querySelector("#var-Ksᵖ").value)
        Kiᵖ = 1

        if Fᵖ < 50: kmᵖ = 1.6
        if Fᵖ < 150: kmᵖ = 1.7
        if Fᵖ < 250: kmᵖ = 1.8
        if Fᵖ < 500: kmᵖ = 1.9
        if Fᵖ >= 500: kmᵖ = 2

        torqᵍ = (60*75*potᵍ)/(2*3.14*rpmᵍ)
        torqᵖ = (60*75*potᵖ)/(2*3.14*rpmᵖ)

        if (document.querySelector("#var-dᵍ input").value):
            rᵍ = float(document.querySelector("#var-dᵍ input").value) / 2
        else:
            rᵍ = float(document.querySelectorAll("#row-dᵍ td")[1].innerHTML) / 2

        if (document.querySelector("#var-dᵖ input").value):
            rᵖ = float(document.querySelector("#var-dᵖ input").value) / 2
        else:
            rᵖ = float(document.querySelectorAll("#row-dᵖ td")[1].innerHTML) / 2

        Wtᵍ = torqᵍ / rᵍ
        Wtᵖ = torqᵖ / rᵖ

        flex_agmaᵍ = (Wtᵍ / (Fᵍ * mᵍ * Jᵍ)) * ((Kaᵍ * kmᵍ) / kvᵍ) * (Kbᵍ + Ksᵍ + Kiᵍ)
        flex_agmaᵖ = (Wtᵖ / (Fᵖ * mᵖ * Jᵖ)) * ((Kaᵖ * kmᵖ) / kvᵖ) * (Kbᵖ + Ksᵖ + Kiᵖ)

        gear = {
            "kmg": [kmg, 'Fator dinámico'],
            "kvg": [kvg, 'Fator dinámico'],
            "Kag": [Kag, 'Fator dinámico'],
            "Kig": [Kig, 'Fator dinámico'],
            "Kbp": [Kbp, 'Fator dinámico'],
            "Ksg": [Ksg, 'Fator dinámico'],
            "Ag": [Ag, ''],
            "Bg": [Bg, ''],
            "mbg": [mbg, 'Razão de recuo'],
            "Qvg": [Qvg, 'Qualidade Engre.'],
            "σ": [flex_agmaᵍ, 'Tensão de Flexão'],
        }

        pinion = {
            "kmp": [kmp, 'Fator dinámico'],
            "kvp": [kvp, 'Fator dinámico'],
            "Kap": [Kap, 'Fator dinámico'],
            "Kip": [Kip, 'Fator dinámico'],
            "Kbp": [Kbp, 'Fator dinámico'],
            "Ksp": [Ksp, 'Fator dinámico'],
            "Ap": [Ap, ''],
            "Bp": [Bp, ''],
            "mbp": [mbp, 'Razão de recuo'],
            "Qvp": [Qvp, 'Qualidade Engre.'],
            "σ": [flex_agmap, 'Tensão de Flexão'],
        }

        div = document.querySelector("#second_section .calculated_values")
        div.innerHTML = """
<section>
  <table class="gear">
    <tbody>
      <tr>
          <th>Simbolo</th>
          <th>Valor</th>
          <th>nome</th>
      </tr>
    </tbody>
  </table>
  <table class="pinion">
    <tbody>
      <tr>
          <th>Simbolo</th>
          <th>Valor</th>
          <th>nome</th>
      </tr>
    </tbody>
  </table>
  <table class="tension">
    <tbody>
      <tr>
          <th>Simbolo</th>
          <th>Valor</th>
          <th>nome</th>
      </tr>
    </tbody>
  </table>
</section>
"""

        gear_results = document.querySelector("#second_section table.gear tbody")
        for key, value in gear.items():
            gear_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])
            
        pinion_results = document.querySelector("#second_section table.pinion tbody")
        for key, value in pinion.items():
            pinion_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])

        mat_1 = int(document.querySelector("#material_1").value)
        mat_2 = int(document.querySelector("#material_2").value)
        pos = int(document.querySelector("#teeth_position").value)

        values = [
            191, 181, 179, 174, 162, 158, 181, 174, 172, 168, 158, 154, 179, 172, 170, 166, 156, 152, 174, 168, 166, 163, 154, 149, 162, 158, 156, 154, 145, 141, 158, 154, 152, 149, 141, 137
        ]
        Cᵖ = values[mat_1 * 6 + mat_2]

        θ = int(document.querySelector("#angle").value)
        C = float(document.querySelector("#centers").innerHTML)
        Pdᵖ = float(document.querySelectorAll("#row-Pdᵖ td")[1].innerHTML) if (document.querySelectorAll("#row-Pdᵖ td")) else float(document.querySelector("#var-Pdᵖ input").value)
        dᵍ = float(document.querySelectorAll("#row-dᵍ td")[1].innerHTML) if (document.querySelectorAll("#row-dᵍ td")) else float(document.querySelector("#var-dᵍ input").value)
        dᵖ = float(document.querySelectorAll("#row-dᵖ td")[1].innerHTML) if (document.querySelectorAll("#row-dᵖ td")) else float(document.querySelector("#var-dᵖ input").value)

        Pᵖ = ((rᵖ + 1 / Pdᵖ) ** 2 - (rᵖ * sp.cos(θ)) ** 2) ** (1/2) - (sp.pi / Pdᵖ) * sp.cos(θ)
        Pᵍ = C * sp.sin(θ) + (pos + Pᵖ)
        I = sp.cos(θ) / ((1/Pᵖ + (1 * pos)/Pᵍ) * dᵖ)

        σcᵖ = Cᵖ * ((Wtᵖ / (Fᵖ * I * dᵖ)) * ((Kaᵖ * kmᵖ) / kvᵖ) * Ksᵖ * 1) ** (1/2)
        σcᵍ = Cᵖ * ((Wtᵍ / (Fᵍ * I * dᵍ)) * ((Kaᵍ * kmᵍ) / kvᵍ) * Ksᵍ * 1) ** (1/2)

        tension = {
            "Pᵖ": [Pᵖ, 'Raio de Curvatura'],
            "Pᵍ": [Pᵍ, 'Raio de Curvatura'],
            "I": [I, 'Fator Geométrico'],
            "σcᵖ": [σcᵖ, 'Tensão Superficial'],
            "σcᵍ": [σcᵍ, 'Tensão Superficial'],
        }

        tension_results = document.querySelector("#second_section table.tension tbody")
        for key, value in tension.items():
            tension_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])
        third_inputs()

    except sp.SympifyError:
      pass


def third_inputs():
    metric_units = ['F', 'variavel', 'variavel']

    gear = document.querySelector("#third_section .gear")
    pinion = document.querySelector("#third_section .pinion")

    render_inputs(gear, variables_g_3, metric_units)
    render_inputs(pinion, variables_p_3, metric_units)

    gear.innerHTML += """
<label>
  <span>Kr, confiabilidade</span>
  <select id="kr_valueᵍ">
    <option value= 0.85>90%</option>
    <option value= 1>99%</option>
    <option value= 1.25>99,9%</option>
    <option value= 1.5>99,99%</option>
  </select>
</label>
<label>
  <span>HBᵍ, Dureza Brinel Gear</span>
  <select id="HBᵍ_value">
    <option value= 160>160</option>
    <option value= 250>250</option>
    <option value= 400>400</option>
  </select>
</label>
"""

    pinion.innerHTML += """
<label>
  <span>Kr, confiabilidade</span>
  <select id="kr_valueᵖ">
    <option value= 0.85>90%</option>
    <option value= 1>99%</option>
    <option value= 1.25>99,9%</option>
    <option value= 1.5>99,99%</option>
  </select>
</label>
<label>
  <span>HBᵖ, Dureza_Brinel Pinio</span>
  <select id="HBᵖ_value">
    <option value= 160>160</option>
    <option value= 250>250</option>
    <option value= 400>400</option>
  </select>
</label>
"""


def calc_third():
    try:
        elements = document.querySelectorAll("#third_section input")
        counter = 0

        Tᵍ, N_cicleᵍ, Sfb_linha_ᵍ = variables_g_3
        Tᵖ, N_cicleᵖ, Sfb_linha_ᵖ = variables_p_3

        for element in elements:
            value_as_sympy = sp.sympify(element.value)
            if (counter == 0): Tᵍ = value_as_sympy
            if (counter == 1): N_cicleᵍ = value_as_sympy
            if (counter == 2): Sfb_linha_ᵍ = value_as_sympy
            if (counter == 3): Tᵖ = value_as_sympy
            if (counter == 4): N_cicleᵖ = value_as_sympy
            if (counter == 5): Sfb_linha_ᵖ = value_as_sympy
            counter += 1

        hbᵍ = float(document.querySelector("#HBᵍ_value").value)
        hbᵖ = float(document.querySelector("#HBᵖ_value").value)

        if (hbᵍ == 400): Klᵍ = 9.4518 * N_cicleᵍ ** -0.148
        if (hbᵍ == 250): Klᵍ = 4.9404 * N_cicleᵍ ** -0.1192
        if (hbᵍ == 160): Klᵍ = 2.3194 * N_cicleᵍ ** -0.1045

        if (hbᵖ == 400): Klᵖ = 9.4518 * N_cicleᵖ ** -0.148
        if (hbᵖ == 250): Klᵖ = 4.9404 * N_cicleᵖ ** -0.1192
        if (hbᵖ == 160): Klᵖ = 2.3194 * N_cicleᵖ ** -0.1045

        Ktᵍ = 1 if (Tᵍ < 250) else (460 + Tᵍ) / 620
        Ktᵖ = 1 if (Tᵖ < 250) else (460 + Tᵖ) / 620
        Krᵍ = float(document.querySelector("#kr_valueᵍ").value)
        Krᵖ = float(document.querySelector("#kr_valueᵖ").value)

        Sfbᵍ = (Klᵍ / (Ktᵍ * Krᵍ)) * Sfb_linha_ᵍ
        Sfbᵖ = (Klᵖ / (Ktᵖ * Krᵖ)) * Sfb_linha_ᵖ

        div = document.querySelector("#third_section .calculated_values")
        div.innerHTML = """
<section>
  <table class="gear">
    <tbody>
      <tr>
          <th>Simbolo</th>
          <th>Valor</th>
          <th>nome</th>
      </tr>
    </tbody>
  </table>
  <table class="pinion">
    <tbody>
      <tr>
          <th>Simbolo</th>
          <th>Valor</th>
          <th>nome</th>
      </tr>
  </tbody>
</section>
"""

        gear = {
            "Ktᵍ": [Ktᵍ, 'Fator Dinámico'],
            "Krᵍ": [Krᵍ, 'Fator Dinámico'],
            "Klᵍ": [Klᵍ, 'Fator Dinámico'],
            "Sfbᵍ": [Sfbᵍ, 'Tabelado']
        }
        pinion = {
            "Ktᵖ": [Ktᵖ, 'Fator Dinámico'],
            "Krᵖ": [Krᵖ, 'Fator Dinámico'],
            "Klᵖ": [Klᵖ, 'Fator Dinámico'],
            "Sfbᵖ": [Sfbᵖ, 'Tabelado']
        }

        gear_results = document.querySelector("#third_section table.gear tbody")
        for key, value in gear.items():
            gear_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])
            
        pinion_results = document.querySelector("#third_section table.pinion tbody")
        for key, value in pinion.items():
            pinion_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])

    except sp.SympifyError:
        pass

