from js import document

container = document.querySelector("#main")
names = ["first", "second", "third"]


def create_inputs(container, names, metric_units, title, classes):
    container.innerHTML = """<legend>{}</legend>""".format(title)
    for i in range(len(names)):
        container.innerHTML += """
<label for="{}">
  <span>{}</span>
  <input
    id="{}"
    class="{} {} {}"
    placeholder="{}"
    oninput="handleInputChange(this)"
  >
</label>
""".format(
            names[i], names[i], names[i], classes[0], classes[1], metric_units[i], metric_units[i]
        )


def create_table(name):
    return """
<table class="{}_table">
  <thead>
    <tr>
      <th>Nome</th>
      <th>Valor</th>
      <th>Unidade</th>
    </tr>
  </thead>
  <tbody></tbody>
</table>""".format(name)


def create_stages():
    for i in range(3):
        container.innerHTML += """
<section id="{}-container" class="wrapper">
    <h2>Parte {}</h2>
    <main>
      <form class="inputs">
        <fieldset class="gear_inputs">
          <legend>Engrenagens</legend>
        </fieldset>
        <fieldset class="pinion_inputs">
          <legend>Pinhão</legend>
        </fieldset>
        <fieldset class="mutual_inputs">
          <legend>Global</legend>
        </fieldset>
      </form>
      <div class="tables">
        <div class="gear table">
          <h4>Engrenagem</h4>
          {}
        </div>
        <div class="pinion table">
          <h4>Pinhão</h4>
          {}
        </div>
        <div class="mutual table">
          <h4>Mútuo</h4>
          {}
        </div>
    </main>
    <button type="button" py-click="calc_first()">calcular</button>
</section>""".format(names[i], i + 1, create_table("gear"), create_table("pinion"), create_table("mutual"))


def render_first_select(mutual_container):
    mutual_container.innerHTML += """
<label for="θ">
  <span>Angulo:</span>
  <select id="θ" class="mutual_values first graus" onclick="handleInputChange(this)">
    <option value="0.3490659">20º</option>
    <option value="0.4363323">25º</option>
  </select>
</label>
"""


def render_second_select(gear_container, pinion_container, mutual_container):
    gear_container.innerHTML += """
<div id="gear-select">
  <label for="gear-motor-shock">
    <span>Maquina Motora</span>
    <select id="gear-motor-shock" class="gear_values second variavel" onclick="handleInputChange(this)">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="2">Choque medio</option>
    </select>
  </label>
  <label for="gear-movable-shock">
    <span>Maquina Movida</span>
    <select id="gear-movable-shock" class="gear_values second variavel" onclick="handleInputChange(this)">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="3">Choque medio</option>
    </select>
  </label>
</div>
<label for="var-Ksᵍ">
  <span>Ksᵍ</span>
  <select id="var-Ksᵍ" class="gear_values second variavel" onclick="handleInputChange(this)">
    <option value="1">1</option>
    <option value="1.25">1.25</option>
    <option value="1.5">1.5</option>
  </select>
</label>
"""

    pinion_container.innerHTML += """
<div id="pinion-select">
  <label for="pinion-motor-shock">
    <span>Maquina Motora</span>
    <select id="pinion-motor-shock" class="pinion_values second variavel" onclick="handleInputChange(this)">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="2">Choque medio</option>
    </select>
  </label>
  <label for="pinion-movable-shock">
    <span>Maquina Movida</span>
    <select id="pinion-movable-shock" class="pinion_values second variavel" onclick="handleInputChange(this)">
      <option value="0">Uniforme</option>
      <option value="1">Choque leve</option>
      <option value="3">Choque medio</option>
    </select>
  </label>
</div>
<label for="var-Ksᵖ">
  <span>Ksᵖ</span>
  <select id="var-Ksᵖ" class="pinion_values second variavel" onclick="handleInputChange(this)">
    <option value="1">1</option>
    <option value="1.25">1.25</option>
    <option value="1.5">1.5</option>
  </select>
</label>
"""

    mutual_container.innerHTML += """
<label for="material_1">
  <span>Material 1</span>
  <select id="material_1" class="mutual_values second variavel" onclick="handleInputChange(this)">
    <option value="0">Aço</option>
    <option value="1">Ferro maleável</option>
    <option value="2">Ferro nodular</option>
    <option value="3">Ferro fundido</option>
    <option value="4">Alumínio bronze</option>
    <option value="5">Estanho bronze</option>
  </select>
</label>
<label for="material_2">
  <span>Material 2</span>
  <select id="material_2" class="mutual_values second variavel" onclick="handleInputChange(this)">
    <option value="0">Aço</option>
    <option value="1">Ferro maleável</option>
    <option value="2">Ferro nodular</option>
    <option value="3">Ferro fundido</option>
    <option value="4">Alumínio bronze</option>
    <option value="5">Estanho bronze</option>
  </select>
</label>
<label for="teeth_position">
  <span>Posição dos Dentes</span>
  <select id="teeth_position" class="mutual_values second variavel" onclick="handleInputChange(this)">
    <option value="1">Externo</option>
    <option value="-1">Interno</option>
  </select>
</label>
"""


def render_third_select(gear_container, pinion_container):
    gear_container.innerHTML += """
<label for="kr_valueᵍ">
  <span>Kr, confiabilidade</span>
  <select id="kr_valueᵍ" class="gear_values third variavel" onclick="handleInputChange(this)">
    <option value="0.85">90%</option>
    <option value="1">99%</option>
    <option value="1.25">99,9%</option>
    <option value="1.5">99,99%</option>
  </select>
</label>

<label for="HBᵍ_value">
  <span>HBᵍ, Dureza Brinel Gear</span>
  <select id="HBᵍ_value" class="gear_values third variavel" onclick="handleInputChange(this)">
    <option value="160">160</option>
    <option value="250">250</option>
    <option value="400">400</option>
  </select>
</label>
"""

    pinion_container.innerHTML += """
<label for="kr_valueᵖ">
  <span>Kr, confiabilidade</span>
  <select id="kr_valueᵖ" class="pinion_values third variavel" onclick="handleInputChange(this)">
    <option value="0.85">90%</option>
    <option value="1">99%</option>
    <option value="1.25">99,9%</option>
    <option value="1.5">99,99%</option>
  </select>
</label>
<label for="HBᵖ_value">
  <span>HBᵖ, Dureza Brinel Pinhão</span>
  <select id="HBᵖ_value" class="pinion_values third variavel" onclick="handleInputChange(this)">
    <option value="160">160</option>
    <option value="250">250</option>
    <option value="400">400</option>
  </select>
</label>
"""
