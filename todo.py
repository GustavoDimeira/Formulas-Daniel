from js import document, global_vars, update_value, get_select_values, console
import json
import sympy as sp
from preset_html import *

meters_to_inches = 0.0254 ** -1
inches_to_milimeters = 25.4

variables_g_1 = sp.symbols("Pc_g Pb_g Pd_g N_g d_g m_g")
variables_p_1 = sp.symbols("Pc_p Pb_p Pd_p N_p d_p m_p")

variables_g_2 = sp.symbols("F_g J_g Qv_g Vt_g tr_g rpm_g pot_g")
variables_p_2 = sp.symbols("F_p J_p Qv_p Vt_p tr_p rpm_p pot_p")

variables_g_3 = sp.symbols("T_g N_cicle_g Sfb_linha__g")
variables_p_3 = sp.symbols("T_p N_cicle_p Sfb_linha__p")

def init():
    create_stages()
    first_inputs(); second_inputs(); third_inputs()
    get_select_values()


def first_inputs():
    metric_units = ['in', 'in', 'in-¹', 'variavel', 'metros', 'milimetros']

    gear = document.querySelector("#first-container .gear_inputs")
    pinion = document.querySelector("#first-container .pinion_inputs")
    mutual = document.querySelector("#first-container .mutual_inputs")

    create_inputs(gear, variables_g_1, metric_units, "Engrenagem", ["gear_values", "first"])
    create_inputs(pinion, variables_p_1, metric_units, "Pinhão", ["pinion_values", "first"])
    render_first_select(mutual)


def second_inputs():
    metric_units = ['in', 'variavel', 'variavel', 'm/s', 'in', 'rpm', 'watts']

    gear = document.querySelector("#second-container .gear_inputs")
    pinion = document.querySelector("#second-container .pinion_inputs")
    mutual =  document.querySelector("#second-container .mutual_inputs")

    create_inputs(gear, variables_g_2, metric_units, "Engrenagem", ["gear_values", "second"])
    create_inputs(pinion, variables_p_2, metric_units, "Pinhão", ["pinion_values", "second"])
    render_second_select(gear, pinion, mutual)


def third_inputs():
    metric_units = ['F', 'variavel', 'variavel']

    gear = document.querySelector("#third-container .gear_inputs")
    pinion = document.querySelector("#third-container .pinion_inputs")

    create_inputs(gear, variables_g_3, metric_units, "Engrenagem", ["gear_values", "third"])
    create_inputs(pinion, variables_p_3, metric_units, "Pinhão", ["pinion_values", "third"])
    render_third_select(gear, pinion)


def calc_first():
    Pc_g, Pb_g, Pd_g, N_g, d_g, m_g = variables_g_1
    Pc_p, Pb_p, Pd_p, N_p, d_p, m_p = variables_p_1

    # if (not global_vars.Pc_g.value == ""): Pc_g = sp.sympify(global_vars.Pc_g.value)
    # if (not global_vars.Pb_g.value == ""): Pb_g = sp.sympify(global_vars.Pb_g.value)
    # if (not global_vars.Pd_g.value == ""): Pd_g = sp.sympify(global_vars.Pd_g.value)
    # if (not global_vars.N_g.value == ""): N_g = sp.sympify(global_vars.N_g.value)
    # if (not global_vars.d_g.value == ""): d_g = sp.sympify(global_vars.d_g.value) * meters_to_inches
    # if (not global_vars.m_g.value == ""): m_g = sp.sympify(global_vars.m_g.value)
    # if (not global_vars.Pc_p.value == ""): Pc_p = sp.sympify(global_vars.Pc_p.value)
    # if (not global_vars.Pb_p.value == ""): Pb_p = sp.sympify(global_vars.Pb_p.value)
    # if (not global_vars.Pd_p.value == ""): Pd_p = sp.sympify(global_vars.Pd_p.value)
    # if (not global_vars.N_p.value == ""): N_p = sp.sympify(global_vars.N_p.value)
    # if (not global_vars.d_p.value == ""): d_p = sp.sympify(global_vars.d_p.value) * meters_to_inches
    # if (not global_vars.m_p.value == ""): m_p = sp.sympify(global_vars.m_p.value)
    # if (not global_vars.θ.value == ""): θ = sp.sympify(global_vars.θ.value)

    N_g = 1
    d_g = 1
    N_p = 1
    d_p = 1
    θ = .5

    equations = [
        sp.Eq(Pc_g, sp.pi * d_g / N_g),
        sp.Eq(Pb_g, Pc_g * sp.cos(θ)),
        sp.Eq(Pd_g, N_g / d_g),
        sp.Eq(m_g, (d_g * inches_to_milimeters) / N_g),
        sp.Eq(Pc_p, sp.pi * d_p / N_p),
        sp.Eq(Pb_p, Pc_p * sp.cos(θ)),
        sp.Eq(Pd_p, N_p / d_p),
        sp.Eq(m_p, (d_p * inches_to_milimeters) / N_p),
    ]

    solution = sp.solve(equations, variables_g_1 + variables_p_1)
    for key in solution:
        try:
            update_value(
                json.dumps([str(solution[key]), False]),
                json.dumps(["first", "pinion", str(key)]),
                True
            )
        except:
            pass

    Pd_g = float(global_vars.Pd_g.value)
    Pd_p = float(global_vars.Pd_p.value)

    gear_list_values = [
        ["adendo", 1/Pd_g, "in-¹"],
        ["dedendo", 1.25/Pd_g, "in-¹"],
        ["profundidade de trabalo", 2/Pd_g, "in-¹"],
        ["profundidade total", 2.25/Pd_g if (1 < 20) else ((2.2/Pd_g) + 0.002), "in-¹"],
        ["espessura circular dente", 1.571/Pd_g, "in-¹"],
        ["raio arredondamento", 0.3/Pd_g if (1 < 20) else "não padronizado", "in-¹"],
        ["folga basica minima", 0.25/Pd_g if (1 < 20) else ((0.2/Pd_g) + 0.002), "in-¹"],
        ["largura minima topo", 0.25/Pd_g if (1 < 20) else "não padronizado", "in-¹"],
        ["folga dentes polidos", 0.35/Pd_g if (1 < 20) else ((0.35/Pd_g) + 0.002), "in-¹"]
    ]

    pinion_list_values = [
        ["adendo", 1/Pd_p, "in-¹"],
        ["dedendo", 1.25/Pd_p, "in-¹"],
        ["profundidade de trabalo", 2/Pd_p, "in-¹"],
        ["profundidade total", 2.25/Pd_p if (1 < 20) else ((2.2/Pd_p) + 0.002), "in-¹"],
        ["espessura circular dente", 1.571/Pd_p, "in-¹"],
        ["raio arredondamento", 0.3/Pd_p if (1 < 20) else "não padronizado", "in-¹"],
        ["folga basica minima", 0.25/Pd_p if (1 < 20) else ((0.2/Pd_p) + 0.002), "in-¹"],
        ["largura minima topo", 0.25/Pd_p if (1 < 20) else "não padronizado", "in-¹"],
        ["folga dentes polidos", 0.35/Pd_p if (1 < 20) else ((0.35/Pd_p) + 0.002), "in-¹"]
    ]

    for name, value, metric in gear_list_values:
        update_value(json.dumps([value, metric]), json.dumps(["first", "gear", str(name)]))

    for name, value, metric in pinion_list_values:
        update_value(json.dumps([value, metric]), json.dumps(["first", "pinion", str(name)]))

    variables_Z_1 = sp.symbols('r_ga_g r_gcos_g r_pa_p r_pcos_p C z')
    r_ga_g, r_gcos_g, r_pa_p, r_pcos_p, c, z = variables_Z_1

    d_g = global_vars.d_g.value
    d_p = global_vars.d_p.value
    c = d_g / 2 + d_p / 2

    r_ga_g = (d_g / 2 + global_vars.adendo.value) ** 2
    r_gcos_g = ((d_g / 2) * sp.cos(θ)) ** 2
    r_pa_p = (d_p / 2 + global_vars.adendo.value) ** 2
    r_pcos_p = ((d_p / 2) * sp.cos(θ)) ** 2

    solution_z = sp.solve(
        sp.Eq(((r_pa_p - r_pcos_p) ** (1/2)) +
              ((r_ga_g - r_gcos_g) ** (1/2)) - (c * sp.sin(θ)), z),
        variables_Z_1
    )

    mp_g = abs(solution_z[0][-1] / solution[Pb_g])
    mp_p = abs(solution_z[0][-1] / solution[Pb_p])

    update_value([c, 'in'], ["first", "mutual_values", 'c'])
    update_value([z, 'variabel'], ["first", "mutual_values", 'z'])
    update_value([mp_g, 'variabel'], ["first", "gear", 'mp_g'])
    update_value([mp_p, 'variabel'], ["first", "pinion", 'mp_p'])


def calc_second():
    try:
        elements = document.querySelectorAll("#second-container input")
        counter = 0

        value_g = document.querySelector("#var-m_g input").value
        value_p = document.querySelector("#var-m_p input").value

        mg = float(value_g) if (value_g) else float(document.querySelectorAll("#row-m_g td")[1].innerHTML)
        mp = float(value_p) if (value_p) else float(document.querySelectorAll("#row-m_p td")[1].innerHTML)

        F_g, J_g, Qv_g, Vt_g, tr_g, rpm_g, pot_g = variables_g_2
        F_p, J_p, Qv_p, Vt_p, tr_p, rpm_p, pot_p = variables_p_2

        for element in elements:
            value_as_sympy = sp.sympify(element.value)
            if (counter == 0): F_g = value_as_sympy
            if (counter == 1): J_g = value_as_sympy
            if (counter == 2): Qv_g = value_as_sympy
            if (counter == 3): Vt_g = value_as_sympy
            if (counter == 4): tr_g = value_as_sympy
            if (counter == 5): rpm_g = value_as_sympy
            if (counter == 6): pot_g = value_as_sympy
            if (counter == 7): F_p = value_as_sympy
            if (counter == 8): J_p = value_as_sympy
            if (counter == 9): Qv_p = value_as_sympy
            if (counter == 10): Vt_p = value_as_sympy
            if (counter == 11): tr_p = value_as_sympy
            if (counter == 12): rpm_p = value_as_sympy
            if (counter == 13): pot_p = value_as_sympy
            counter += 1

        if ((F_g / 8) > m_g): F_g = 8 * m_g
        if ((F_g / 16) < m_g): F_g = 16 * m_g

        if ((F_p / 8) > m_p): F_p = 8 * m_p
        if ((F_p / 16) < m_p): F_p = 16 * m_p

        Qv_g_fpm = Qv_g * 196.850394
        Qv_p_fpm = Qv_p * 196.850394

        if (Vt_g > 0 and Vt_g <= 800):
            if (not Qv_g_fpm >= 6 or not Qv_g_fpm <= 8): Qv_g = 7
        if (Vt_g > 800 and Vt_g <= 2000):
            if (not Qv_g_fpm >= 8 or not Qv_g_fpm <= 10): Qv_g = 9
        if (Vt_g > 2000 and Vt_g <= 4000):
            if (not Qv_g_fpm >= 10 or not Qv_g_fpm <= 12): Qv_g = 11
        if (Vt_g > 4000):
            if (not Qv_g_fpm >= 12 or not Qv_g_fpm <= 14): Qv_g = 13

        if (Vt_p > 0 and Vt_p <= 800):
            if (not Qv_p_fpm >= 6 or not Qv_p_fpm <= 8): Qv_p = 7
        if (Vt_p > 800 and Vt_p <= 2000):
            if (not Qv_p_fpm >= 8 or not Qv_p_fpm <= 10): Qv_p = 9
        if (Vt_p > 2000 and Vt_p <= 4000):
            if (not Qv_p_fpm >= 10 or not Qv_p_fpm <= 12): Qv_p = 11
        if (Vt_p > 4000):
            if (not Qv_p_fpm >= 12 or not Qv_p_fpm <= 14): Qv_p = 13

        B_g = ((12 / Qv_g) ** (2/3)) / 4
        A_g = 50 + 56 * (1 - B_g)
        val_1_g = document.querySelector("#gear-select .motor").value
        val_2_g = document.querySelector("#gear-select .moveable").value
        adendo_g = float(document.querySelectorAll("#table_values .gear #row-adendo td")[1].innerHTML) 
        dedendo_g = float(document.querySelectorAll("#table_values .gear #row-dedendo td")[1].innerHTML)
        mb_g = tr_g / (adendo_g + dedendo_g)

        B_p = ((12 / Qv_p) ** (2/3)) / 4
        A_p = 50 + 56 * (1 - B_p)
        val_1_p = document.querySelector("#pinion-select .motor").value
        val_2_p = document.querySelector("#pinion-select .moveable").value
        adendo_p = float(document.querySelectorAll("#table_values .pinion #row-adendo td")[1].innerHTML)
        dedendo_p = float(document.querySelectorAll("#table_values .pinion #row-dedendo td")[1].innerHTML)
        mb_p = tr_p / (adendo_p + dedendo_p)

        kv_g = (A_g / (A_g + ((200 * Vt_g) ** 1/2))) ** B_g
        Ka_g = 1 + ((int(val_1_g) + int(val_2_g)) * 0.25)
        Kb_g = -2 * mb_g + 3.4 if (mb_g >= 0.5 and mb_g <= 1.2) else 1
        Ks_g = float(document.querySelector("#var-Ks_g").value)
        Ki_g = 1
        
        if F_g < 50: km_g = 1.6
        if F_g < 150: km_g = 1.7
        if F_g < 250: km_g = 1.8
        if F_g < 500: km_g = 1.9
        if F_g >= 500: km_g = 2

        kv_p = (A_p / (A_p + ((200 * Vt_p) ** 1/2))) ** B_p
        Ka_p = 1 + ((int(val_1_p) + int(val_2_p)) * 0.25)
        Kb_p = -2 * mb_p + 3.4 if (mb_p >= 0.5 and mb_p <= 1.2) else 1
        Ks_p = float(document.querySelector("#var-Ks_p").value)
        Ki_p = 1

        if F_p < 50: km_p = 1.6
        if F_p < 150: km_p = 1.7
        if F_p < 250: km_p = 1.8
        if F_p < 500: km_p = 1.9
        if F_p >= 500: km_p = 2

        torq_g = (60*75*pot_g)/(2*3.14*rpm_g)
        torq_p = (60*75*pot_p)/(2*3.14*rpm_p)

        if (document.querySelector("#var-d_g input").value):
            r_g = float(document.querySelector("#var-d_g input").value) / 2
        else:
            r_g = float(document.querySelectorAll("#row-d_g td")[1].innerHTML) / 2

        if (document.querySelector("#var-d_p input").value):
            r_p = float(document.querySelector("#var-d_p input").value) / 2
        else:
            r_p = float(document.querySelectorAll("#row-d_p td")[1].innerHTML) / 2

        Wt_g = torq_g / r_g
        Wt_p = torq_p / r_p

        flex_agma_g = (Wt_g / (F_g * m_g * J_g)) * ((Ka_g * km_g) / kv_g) * (Kb_g + Ks_g + Ki_g)
        flex_agma_p = (Wt_p / (F_p * m_p * J_p)) * ((Ka_p * km_p) / kv_p) * (Kb_p + Ks_p + Ki_p)

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
            "σ": [flex_agma_g, 'Tensão de Flexão'],
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

        div = document.querySelector("#second-container .calculated_values")
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

        gear_results = document.querySelector("#second-container table.gear tbody")
        for key, value in gear.items():
            gear_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])
            
        pinion_results = document.querySelector("#second-container table.pinion tbody")
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
        C_p = values[mat_1 * 6 + mat_2]

        θ = int(document.querySelector("#angle").value)
        C = float(document.querySelector("#centers").innerHTML)
        Pd_p = float(document.querySelectorAll("#row-Pd_p td")[1].innerHTML) if (document.querySelectorAll("#row-Pd_p td")) else float(document.querySelector("#var-Pd_p input").value)
        d_g = float(document.querySelectorAll("#row-d_g td")[1].innerHTML) if (document.querySelectorAll("#row-d_g td")) else float(document.querySelector("#var-d_g input").value)
        d_p = float(document.querySelectorAll("#row-d_p td")[1].innerHTML) if (document.querySelectorAll("#row-d_p td")) else float(document.querySelector("#var-d_p input").value)

        P_p = ((r_p + 1 / Pd_p) ** 2 - (r_p * sp.cos(θ)) ** 2) ** (1/2) - (sp.pi / Pd_p) * sp.cos(θ)
        P_g = C * sp.sin(θ) + (pos + P_p)
        I = sp.cos(θ) / ((1/P_p + (1 * pos)/P_g) * d_p)

        σc_p = C_p * ((Wt_p / (F_p * I * d_p)) * ((Ka_p * km_p) / kv_p) * Ks_p * 1) ** (1/2)
        σc_g = C_p * ((Wt_g / (F_g * I * d_g)) * ((Ka_g * km_g) / kv_g) * Ks_g * 1) ** (1/2)

        tension = {
            "P_p": [P_p, 'Raio de Curvatura'],
            "P_g": [P_g, 'Raio de Curvatura'],
            "I": [I, 'Fator Geométrico'],
            "σc_p": [σc_p, 'Tensão Superficial'],
            "σc_g": [σc_g, 'Tensão Superficial'],
        }

        tension_results = document.querySelector("#second-container table.tension tbody")
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


def calc_third():
    try:
        elements = document.querySelectorAll("#third-container input")
        counter = 0

        T_g, N_cicle_g, Sfb_linha__g = variables_g_3
        T_p, N_cicle_p, Sfb_linha__p = variables_p_3

        for element in elements:
            value_as_sympy = sp.sympify(element.value)
            if (counter == 0): T_g = value_as_sympy
            if (counter == 1): N_cicle_g = value_as_sympy
            if (counter == 2): Sfb_linha__g = value_as_sympy
            if (counter == 3): T_p = value_as_sympy
            if (counter == 4): N_cicle_p = value_as_sympy
            if (counter == 5): Sfb_linha__p = value_as_sympy
            counter += 1

        hb_g = float(document.querySelector("#HB_g_value").value)
        hb_p = float(document.querySelector("#HB_p_value").value)

        if (hb_g == 400): Kl_g = 9.4518 * N_cicle_g ** -0.148
        if (hb_g == 250): Kl_g = 4.9404 * N_cicle_g ** -0.1192
        if (hb_g == 160): Kl_g = 2.3194 * N_cicle_g ** -0.1045

        if (hb_p == 400): Kl_p = 9.4518 * N_cicle_p ** -0.148
        if (hb_p == 250): Kl_p = 4.9404 * N_cicle_p ** -0.1192
        if (hb_p == 160): Kl_p = 2.3194 * N_cicle_p ** -0.1045

        Kt_g = 1 if (T_g < 250) else (460 + T_g) / 620
        Kt_p = 1 if (T_p < 250) else (460 + T_p) / 620
        Kr_g = float(document.querySelector("#kr_value_g").value)
        Kr_p = float(document.querySelector("#kr_value_p").value)

        Sfb_g = (Kl_g / (Kt_g * Kr_g)) * Sfb_linha__g
        Sfb_p = (Kl_p / (Kt_p * Kr_p)) * Sfb_linha__p

        div = document.querySelector("#third-container .calculated_values")
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
            "Kt_g": [Kt_g, 'Fator Dinámico'],
            "Kr_g": [Kr_g, 'Fator Dinámico'],
            "Kl_g": [Kl_g, 'Fator Dinámico'],
            "Sfb_g": [Sfb_g, 'Tabelado']
        }

        pinion = {
            "Kt_p": [Kt_p, 'Fator Dinámico'],
            "Kr_p": [Kr_p, 'Fator Dinámico'],
            "Kl_p": [Kl_p, 'Fator Dinámico'],
            "Sfb_p": [Sfb_p, 'Tabelado']
        }

        gear_results = document.querySelector("#third-container table.gear tbody")
        for key, value in gear.items():
            gear_results.innerHTML += """
<tr id="row-{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(key, key, round(value[0], 4), value[1])
            
        pinion_results = document.querySelector("#third-container table.pinion tbody")
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


init()
