import math
import re

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)
        self.expression = ""

        self.display = Label(
            text="0",
            halign="right",
            valign="middle",
            text_size=(self.width * 0.9, None),
            font_size="40sp",
            size_hint=(1, 0.2),
            color=(0.8, 0.87, 0.96, 1),
        )
        self.add_widget(self.display)

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]

        grid = GridLayout(cols=4, spacing=6, size_hint=(1, 0.8))
        for row in buttons:
            for text in row:
                if text in ("÷", "×", "-", "+", "="):
                    bg = (0.96, 0.55, 0.55, 1)
                elif text == "C":
                    bg = (0.54, 0.6, 0.96, 1)
                else:
                    bg = (0.19, 0.2, 0.27, 1)
                btn = Button(
                    text=text,
                    font_size="28sp",
                    background_normal="",
                    background_color=bg,
                    color=(0.8, 0.87, 0.96, 1),
                    on_press=self.on_button,
                )
                grid.add_widget(btn)

        self.add_widget(grid)

    def on_button(self, instance):
        char = instance.text
        if char == "C":
            self.expression = ""
            self.display.text = "0"
            return

        if char == "⌫":
            self.expression = self.expression[:-1]
            self.display.text = self.expression if self.expression else "0"
            return

        if char == "±":
            if self.expression:
                try:
                    val = float(self.expression)
                    self.expression = str(-val).rstrip("0").rstrip(".")
                    self.display.text = self.expression
                except ValueError:
                    pass
            return

        if char == "=":
            self.calculate()
            return

        self.expression += char
        self.display.text = self.expression

    def calculate(self):
        if not self.expression:
            return
        try:
            expr = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(expr, {"__builtins__": {}}, {"math": math})
            if isinstance(result, float) and result == int(result) and abs(result) < 1e15:
                display = str(int(result))
            elif isinstance(result, float):
                display = f"{result:.10g}"
            else:
                display = str(result)
            self.expression = display
            self.display.text = display
        except ZeroDivisionError:
            self.display.text = "Error"
            self.expression = ""
        except Exception:
            self.display.text = "Error"
            self.expression = ""


class CalculatorApp(App):
    def build(self):
        Window.clearcolor = (0.12, 0.12, 0.18, 1)
        return CalculatorLayout()


if __name__ == "__main__":
    CalculatorApp().run()
