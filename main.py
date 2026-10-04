import streamlit as st
import math

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Scientific Calculator")

# Session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []


# Safe math functions
allowed_functions = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "factorial": math.factorial,
    "pi": math.pi,
    "e": math.e
}


def calculate(expression):
    """
    Calculate mathematical expression using allowed
    math functions and constants.
    """

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            allowed_functions
        )

        return result

    except ZeroDivisionError:
        return "Cannot divide by zero"

    except Exception:
        return "Invalid expression"


# Keyboard input
keyboard_input = st.text_input(
    "Enter expression",
    value=st.session_state.expression,
    placeholder="Example: sqrt(25) + 10 * 2"
)

st.session_state.expression = keyboard_input


# Mouse buttons
st.write("### Calculator")

buttons = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["sqrt(", "sin(", "cos(", "tan("],
    ["log(", "ln(", "^", "π"]
]


for row in buttons:
    cols = st.columns(4)

    for i, button in enumerate(row):

        with cols[i]:

            if st.button(
                button,
                key=f"button_{button}_{buttons.index(row)}_{i}",
                use_container_width=True
            ):

                if button == "C":
                    st.session_state.expression = ""

                elif button == "⌫":
                    st.session_state.expression = (
                        st.session_state.expression[:-1]
                    )

                elif button == "=":

                    expression = st.session_state.expression

                    if expression:

                        result = calculate(expression)

                        if isinstance(result, (int, float)):

                            st.session_state.history.append(
                                f"{expression} = {result}"
                            )

                            st.session_state.expression = str(result)

                        else:
                            st.error(result)

                elif button == "π":
                    st.session_state.expression += "pi"

                else:
                    st.session_state.expression += button


# Display current expression
st.text_input(
    "Calculator",
    value=st.session_state.expression,
    disabled=True
)


# History
if st.session_state.history:

    st.write("### History")

    for item in reversed(st.session_state.history[-10:]):
        st.write(item)