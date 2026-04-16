from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.core.window import Window

# Fixed: Use "" to avoid the ValueError
Window.softinput_mode = ""

class LumberApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        self.active_input = None

        screen = Screen()

        # Root layout: stacked top to bottom
        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5), 
            padding=dp(10)
        )

        # ================= 1. DISPLAY (TOP) =================
        display = MDBoxLayout(
            size_hint=(1, None),
            height=dp(90),
            padding=[dp(15), dp(10), dp(15), dp(10)],
            md_bg_color=(0, 0, 0, 1)
        )

        self.result = MDLabel(
            text="0.00",
            halign="right",
            valign="middle",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1)
        )

        display.add_widget(self.result)
        root.add_widget(display)

        # ================= 2. INPUT AREA (MIDDLE) =================
        input_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(215), # Slightly adjusted to fit new row spacing
            spacing=dp(8)   # Increased vertical gap between L, W, H rows
        )

        def create_field(hint):
            field = MDTextField(
                hint_text=hint,
                readonly=True, 
                mode="rectangle",
                size_hint=(1, None),
                height=dp(42)
            )
            field.bind(on_touch_down=self.set_active_touch)
            return field

        def row(label):
            box = MDBoxLayout(
                size_hint=(1, None),
                height=dp(45),
                spacing=dp(15) # ✅ Increased gap between ft and in textboxes
            )

            lbl = MDLabel(
                text=label,
                size_hint=(0.15, 1),
                bold=True
            )

            ft = create_field("ft")
            inch = create_field("in")

            box.add_widget(lbl)
            box.add_widget(ft)
            box.add_widget(inch)

            return box, ft, inch

        self.len_row, self.len_ft, self.len_in = row("L")
        self.wid_row, self.wid_ft, self.wid_in = row("W")
        self.hei_row, self.hei_ft, self.hei_in = row("H")

        # Increased horizontal spacing for Qty and Rate too
        extra_row = MDBoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(15))
        self.qty = create_field("Qty")
        self.rate = create_field("Rate")
        extra_row.add_widget(self.qty)
        extra_row.add_widget(self.rate)

        input_box.add_widget(self.len_row)
        input_box.add_widget(self.wid_row)
        input_box.add_widget(self.hei_row)
        input_box.add_widget(extra_row)

        root.add_widget(input_box)

        # ================= 3. KEYPAD (BOTTOM) =================
        keypad = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1), 
            spacing=dp(5)
        )

        keys = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [".", "0", "⌫"]
        ]

        for row_keys in keys:
            row_box = MDBoxLayout(size_hint=(1, 1), spacing=dp(5))
            for k in row_keys:
                btn = MDRaisedButton(
                    text=k,
                    size_hint=(1, 1),
                    font_size="20sp",
                    on_release=self.key_press
                )
                row_box.add_widget(btn)
            keypad.add_widget(row_box)

        # ================= ENTER + CLEAR =================
        bottom = MDBoxLayout(
            size_hint=(1, None),
            height=dp(55),
            spacing=dp(8)
        )

        btn_enter = MDRaisedButton(
            text="ENTER",
            size_hint=(0.7, 1),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.calculate
        )

        btn_clear = MDFlatButton(
            text="CLEAR",
            size_hint=(0.3, 1),
            on_release=self.clear
        )

        bottom.add_widget(btn_enter)
        bottom.add_widget(btn_clear)

        keypad.add_widget(bottom)
        root.add_widget(keypad)

        screen.add_widget(root)
        return screen

    def set_active_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.active_input = instance
            for field in [self.len_ft, self.len_in, self.wid_ft, self.wid_in, 
                          self.hei_ft, self.hei_in, self.qty, self.rate]:
                field.line_color_normal = (0.5, 0.5, 0.5, 1)
            instance.line_color_normal = (0, 1, 0, 1)
            return True
        return False

    def key_press(self, obj):
        if not self.active_input: return
        if obj.text == "<<":
            self.active_input.text = self.active_input.text[:-1]
        else:
            self.active_input.text += obj.text

    def to_ft(self, ft, inch):
        try:
            return float(ft or 0) + float(inch or 0) / 12
        except:
            return 0.0

    def calculate(self, obj):
        try:
            L = self.to_ft(self.len_ft.text, self.len_in.text)
            W = self.to_ft(self.wid_ft.text, self.wid_in.text)
            H = self.to_ft(self.hei_ft.text, self.hei_in.text)
            qty = int(self.qty.text or 1)
            rate = float(self.rate.text or 0)

            volume = L * W * H * qty
            total = volume * rate
            self.result.text = f"{volume:.2f} ft³\n{total:.2f}/-"
        except:
            self.result.text = "ERROR"

    def clear(self, obj):
        for w in [self.len_ft, self.len_in, self.wid_ft, self.wid_in, 
                  self.hei_ft, self.hei_in, self.qty, self.rate]:
            w.text = ""
        self.result.text = "0.00"


if __name__ == "__main__":
    LumberApp().run()
