import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- Configuração do Layout da Página ---
st.set_page_config(layout="wide", page_title="Plotador de Funções")

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
        **Marque a opção "É uma circunferência?" para o ajuste correto do gráfico.**
    
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
    
    function_str = st.text_input("Função Principal (em termos de 'x'):", "np.sin(x)", help="Ex: np.sin(x) ou np.sqrt(4 - x**2) para a parte superior do círculo.")
    
    plot_secondary = st.checkbox("Plotar uma segunda função (útil para círculos completos)?")
    secondary_function_str = ""
    if plot_secondary:
        secondary_function_str = st.text_input("Segunda Função (para círculo completo ou outra curva):", "-np.sqrt(4 - x**2)", help="Ex: -np.sqrt(4 - x**2) para a parte inferior do círculo.")
    
    is_circle = st.checkbox("É uma circunferência (para ajuste correto de escala)?", value=False, help="Marque esta opção se estiver plotando um círculo para que ele apareça redondo.")

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
                
                y = eval(function_str, {"np": np}, {"x": x})
                
                # figsize pode ser ajustado para tirar proveito da largura maior, se desejar
                fig, ax = plt.subplots(figsize=(10, 5)) # Exemplo: largura 10, altura 5 para aproveitar o wide
                
                ax.plot(x, y, label=function_str)

                if plot_secondary and secondary_function_str.strip():
                    y_secondary = eval(secondary_function_str, {"np": np}, {"x": x})
                    ax.plot(x, y_secondary, label=secondary_function_str, linestyle='--')

                ax.set_title(f"Gráfico 2D", fontsize=10)
                ax.set_xlabel("x", fontsize=9)
                ax.set_ylabel("y", fontsize=9)
                ax.grid(True)
                ax.legend()
                
                if is_circle:
                    ax.set_aspect('equal', adjustable='box')
                else:
                    ax.set_aspect('auto')
                
                plt.tight_layout()
                
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Erro ao plotar a função 2D: {e}. Verifique a sintaxe da função e os exemplos acima.")

else: # plot_type == "3D"
    st.header("Plotagem 3D")
    st.write("O gráfico 3D é interativo. Você pode arrastar para rotacionar.")

    col1, col2 = st.columns(2)
    with col1:
        x_min_3d = st.number_input("Valor mínimo de x (3D):", value=-5.0, step=0.5)
    with col2:
        y_min_3d = st.number_input("Valor mínimo de y (3D):", value=-5.0, step=0.5)
    
    col3, col4 = st.columns(2) # Usando novas colunas para x_max e y_max
    with col3:
        x_max_3d = st.number_input("Valor máximo de x (3D):", value=5.0, step=0.5)
    with col4:
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
                    height=500 # Altura fixa para o gráfico Plotly 3D
                )
                
                st.plotly_chart(fig, use_container_width=True) # use_container_width=True faz ele usar 100% da largura disponível
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
16. **Círculo Completo (Exemplo de Raio 2):**
    * **Função Principal:** `np.sqrt(4 - x**2)`
    * **Segunda Função:** `-np.sqrt(4 - x**2)`
    * **Limites de X:** `-2.0` a `2.0`
    * **IMPORTANTE:** Marque a caixa "É uma circunferência?"

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