import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="centered", page_title="Plotador de Funções")

st.title("Plotador de Funções 2D e 3D")

# --- Seleção do Tipo de Plotagem ---
plot_type = st.radio("Escolha o tipo de plotagem:", ("2D", "3D"))

st.write("---")

# --- Input da Função com Descrições ---
st.subheader("Insira sua Função")

if plot_type == "2D":
    st.write("Use **'x'** como sua variável.")
    st.markdown("""
    **Sintaxe de Exemplo:**
    * **Funções Básicas:** `np.sin(x)`, `x**2`, `np.exp(-x**2)`
    * **Círculo Completo:** Para uma circunferência, você precisará de duas funções:
        1. Parte Superior: `np.sqrt(R**2 - x**2)`
        2. Parte Inferior: `-np.sqrt(R**2 - x**2)`
        Onde `R` é o raio do círculo. Defina os limites de `x` de `-R` a `R`.
    
    **Outras Sintaxes:**
    * **Raiz Quadrada:** `np.sqrt(x)` ou `x**0.5`
    * **Exponenciação:** `x**2` (x ao quadrado), `x**3` (x ao cubo), etc.
    * **Funções Trigonométricas:** `np.sin(x)`, `np.cos(x)`, `np.tan(x)`
    * **Exponencial (e^x):** `np.exp(x)`
    * **Logaritmo Natural (ln):** `np.log(x)` (logaritmo na base e)
    * **Logaritmo Base 10:** `np.log10(x)`
    * **Constantes:** `np.pi` (Pi), `np.e` (Número de Euler)
    * **Operações Básicas:** `+`, `-`, `*`, `/`
    """)
    
    # Input para a primeira função
    function_str = st.text_input("Função Principal (em termos de 'x'):", "np.sin(x)", help="Ex: np.sin(x) ou np.sqrt(4 - x**2) para a parte superior do círculo.")
    
    # Input opcional para a segunda função (para círculos)
    plot_secondary = st.checkbox("Plotar uma segunda função (útil para círculos completos)?")
    secondary_function_str = ""
    if plot_secondary:
        secondary_function_str = st.text_input("Segunda Função (para círculo completo ou outra curva):", "-np.sqrt(4 - x**2)", help="Ex: -np.sqrt(4 - x**2) para a parte inferior do círculo.")

else: # 3D
    st.write("Use **'x'** e **'y'** como suas variáveis.")
    st.markdown("""
    **Sintaxe de Exemplo:**
    * **Raiz Quadrada:** `np.sqrt(x**2 + y**2)`
    * **Exponenciação:** `x**2 + y**2`
    * **Funções Trigonométricas:** `np.sin(x)`, `np.cos(y)`
    * **Exponencial (e^(x+y)):** `np.exp(x + y)`
    * **Logaritmo Natural (ln):** `np.log(x)`
    * **Constantes:** `np.pi` (Pi), `np.e` (Número de Euler)
    * **Operações Básicas:** `+`, `-`, `*`, `/`
    
    **Exemplos:** `np.sin(np.sqrt(x**2 + y**2))`, `x*y`, `np.exp(-(x**2 + y**2))`
    """)
    
    function_str = st.text_input("Função (em termos de 'x' e 'y'):", "np.sin(np.sqrt(x**2 + y**2))")

st.write("---")

if plot_type == "2D":
    st.header("Plotagem 2D")

    # Limites do eixo X
    col1, col2 = st.columns(2)
    with col1:
        x_min = st.number_input("Valor mínimo de x:", value=-5.0, step=0.5)
    with col2:
        x_max = st.number_input("Valor máximo de x:", value=5.0, step=0.5)

    if st.button("Plotar Gráfico 2D"):
        if not function_str.strip():
            st.warning("Por favor, insira uma função para plotar.")
        else:
            try:
                x = np.linspace(x_min, x_max, 500)
                
                # Plotar a função principal
                y = eval(function_str, {"np": np}, {"x": x})
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.plot(x, y, label=function_str) # Adiciona label para a legenda

                # Plotar a segunda função, se fornecida
                if plot_secondary and secondary_function_str.strip():
                    y_secondary = eval(secondary_function_str, {"np": np}, {"x": x})
                    ax.plot(x, y_secondary, label=secondary_function_str, linestyle='--') # Linha tracejada para diferenciar

                ax.set_title(f"Gráfico 2D", fontsize=10)
                ax.set_xlabel("x", fontsize=9)
                ax.set_ylabel("y", fontsize=9)
                ax.grid(True)
                ax.legend() # Mostra a legenda com os nomes das funções
                ax.set_aspect('equal', adjustable='box') # Isso é crucial para que círculos pareçam círculos
                plt.tight_layout()
                
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Erro ao plotar a função 2D: {e}. Verifique a sintaxe da função e os exemplos acima.")

else: # plot_type == "3D"
    st.header("Plotagem 3D")
    st.write("O gráfico 3D é interativo. Você pode arrastar para rotacionar.")

    # Limites dos eixos X e Y
    col1, col2 = st.columns(2)
    with col1:
        x_min_3d = st.number_input("Valor mínimo de x (3D):", value=-5.0, step=0.5)
        x_max_3d = st.number_input("Valor máximo de x (3D):", value=5.0, step=0.5)
    with col2:
        y_min_3d = st.number_input("Valor mínimo de y (3D):", value=-5.0, step=0.5)
        y_max_3d = st.number_input("Valor máximo de y (3D):", value=5.0, step=0.5)

    if st.button("Plotar Gráfico 3D"):
        if not function_str.strip():
            st.warning("Por favor, insira uma função para plotar.")
        else:
            try:
                x = np.linspace(x_min_3d, x_max_3d, 50)
                y = np.linspace(y_min_3d, y_max_3d, 50)
                X, Y = np.meshgrid(x, y)

                Z = eval(function_str, {"np": np}, {"x": X, "y": Y})

                fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='viridis')])
                
                fig.update_layout(
                    title=f"Gráfico de Z = {function_str}",
                    scene=dict(
                        xaxis_title='x',
                        yaxis_title='y',
                        zaxis_title='Z',
                    ),
                    margin=dict(l=0, r=0, b=0, t=40),
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao plotar a função 3D: {e}. Verifique a sintaxe da função e os exemplos acima.")



### Exemplos de Funções para o Usuário

st.subheader("30 Exemplos de Funções para Experimentar")

st.markdown("""
**Funções 2D:**
1.  `x**2` (Parábola)
2.  `np.sin(x)` (Onda Senoidal)
3.  `np.cos(x)` (Onda Cosseno)
4.  `np.exp(-x**2)` (Curva de Sino/Gaussiana)
5.  `1/x` (Hipérbole)
6.  `np.log(x)` (Logaritmo Natural)
7.  `np.tan(x)` (Tangente)
8.  `np.sqrt(x)` (Raiz Quadrada)
9.  `x**3` (Cúbica)
10. `abs(x)` (Valor Absoluto)
11. `np.sin(x)/x` (Função Sinc)
12. `np.round(x)` (Arredondamento)
13. `np.floor(x)` (Parte Inteira)
14. `np.ceil(x)` (Teto)
15. `2*x + 1` (Linha Reta)

**Funções 3D:**
1.  `x**2 + y**2` (Paraboloide)
2.  `np.sin(np.sqrt(x**2 + y**2))` (Onda Circular)
3.  `x*y` (Sela)
4.  `np.exp(-(x**2 + y**2))` (Montanha Gaussiana)
5.  `np.sin(x) + np.cos(y)` (Onda Composta)
6.  `np.sqrt(x**2 + y**2)` (Cone Invertido)
7.  `np.sin(x) * np.cos(y)` (Padrão de Ondas)
8.  `x**2 - y**2` (Paraboloide Hiperbólico)
9.  `np.sin(x*y)` (Superfície Ondulada Complexa)
10. `1 / (x**2 + y**2 + 0.1)` (Pico Central)
11. `np.cos(x/2) * np.sin(y/2)`
12. `np.sin(x)**2 + np.cos(y)**2`
13. `(x**2 + y**2)**0.5 * np.sin(np.arctan2(y, x))` (Espiral)
14. `np.cos(x) * np.cos(y) * np.exp(-(x**2 + y**2)/5)`
15. `(x-1)**2 + (y+2)**2` (Paraboloide deslocado)
""")

"""

### O Que Mudou e Como Usar:

1.  **Plotly para 3D:**
    * Substituí a plotagem 3D do Matplotlib por **Plotly**.
    * `import plotly.graph_objects as go` foi adicionado.
    * No bloco `else` (para 3D), você verá `fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='viridis')])` para criar a superfície 3D.
    * `st.plotly_chart(fig, use_container_width=True)` agora exibe o gráfico Plotly.
    * A beleza do Plotly é que ele é **interativo por padrão**. O usuário pode **clicar e arrastar o gráfico 3D para rotacioná-lo, além de dar zoom e pan**.
    * **Removi os sliders de rotação manual para 3D** porque a interatividade do Plotly os torna redundantes e a experiência de arrastar é muito melhor. Adicionei uma nota na interface informando que o gráfico é interativo. Se, por algum motivo, você ainda quiser sliders de controle *estático* (para Matplotlib), posso reinserir, mas não seria a mesma interatividade.
    * A altura do gráfico Plotly é controlada por `height=500` no `fig.update_layout`.

2.  **Lista de Exemplos:**
    * Adicionei um `st.subheader("30 Exemplos de Funções para Experimentar")` e um longo bloco `st.markdown` no final do script.
    * A lista é dividida em exemplos 2D e 3D para facilitar a referência do usuário.

### Para Testar:

1.  **Instale Plotly:** Se ainda não o fez, execute `pip install plotly` no seu terminal.
2.  **Salve e Execute:** Salve o código como `app.py` e execute `streamlit run app.py`.

Agora, ao selecionar a opção "3D", você verá um gráfico que pode ser livremente rotacionado com o mouse, e o usuário terá uma lista rica de exemplos para testar suas próprias funções.

Faz sentido essa abordagem com Plotly para a interatividade 3D?"""