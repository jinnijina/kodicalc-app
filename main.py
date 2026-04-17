from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.core.window import Window

# 🔥 Disable system keyboard completely
Window.softinput_mode = "below_target"
Window.keyboard_mode = "managed"

# Vibrate (works only on Android)
try:
    from plyer import vibrator
    VIBRATE = True
except:
    VIBRATE = False


class LumberApp(MDApp):

    def vibrate(self, ms=30):
        if VIBRATE:
            try:
                vibrator.vibrate(ms)
            except:
                pass

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        self.active_input = None
        self.all_fields = []

        screen = Screen()

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(5)
        )

        # ===== DISPLAY =====
        display = MDBoxLayout(
            size_hint=(1, None),
            height=dp(95),
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

        def add_equal_spacer():
            root.add_widget(MDBoxLayout(size_hint_y=1))

        def create_field(hint):
            field = MDTextField(
                hint_text=hint,
                mode="rectangle",
                readonly=True,
                size_hint=(1, None),
                height=dp(42)
            )

            field.bind(on_touch_down=self.set_active_touch)
            self.all_fields.append(field)
            return field

        def row(label):
            box = MDBoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(15))
            lbl = MDLabel(text=label, size_hint=(0.15, 1), bold=True)
            ft = create_field("ft")
            inch = create_field("in")
            box.add_widget(lbl)
            box.add_widget(ft)
            box.add_widget(inch)
            return box, ft, inch

        add_equal_spacer()

        self.len_row, self.len_ft, self.len_in = row("L")
        root.add_widget(self.len_row)

        add_equal_spacer()

        self.wid_row, self.wid_ft, self.wid_in = row("W")
        root.add_widget(self.wid_row)

        add_equal_spacer()

        self.hei_row, self.hei_ft, self.hei_in = row("H")
        root.add_widget(self.hei_row)

        add_equal_spacer()

        extra_row = MDBoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(15))
        self.qty = create_field("Qty")
        self.rate = create_field("Rate")
        extra_row.add_widget(self.qty)
        extra_row.add_widget(self.rate)
        root.add_widget(extra_row)

        add_equal_spacer()

        # ===== KEYPAD =====
        keypad_container = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(280),
            spacing=dp(8)
        )

        keys = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [".", "0", "<<"]]

        for row_keys in keys:
            row_box = MDBoxLayout(size_hint=(1, 1), spacing=dp(8))
            for k in row_keys:
                btn = MDRaisedButton(
                    text=k,
                    size_hint=(1, 1),
                    font_size="20sp",
                    on_release=self.key_press
                )
                row_box.add_widget(btn)
            keypad_container.add_widget(row_box)

        bottom_btns = MDBoxLayout(size_hint=(1, 1), spacing=dp(10))

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

        bottom_btns.add_widget(btn_enter)
        bottom_btns.add_widget(btn_clear)
        keypad_container.add_widget(bottom_btns)

        root.add_widget(keypad_container)

        screen.add_widget(root)
        return screen

    # ===== TOUCH =====
    def set_active_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.vibrate()

            self.active_input = instance

            for field in self.all_fields:
                field.focus = False
                field.line_color_normal = (0.5, 0.5, 0.5, 1)

            instance.line_color_normal = self.theme_cls.primary_color

            return True
        return False

    # ===== FIXED KEYPAD =====
    def key_press(self, obj):
        if not self.active_input:
            return

        self.vibrate()

        text = self.active_input.text

        if obj.text == "<<":
            self.active_input.text = text[:-1]
            return

        # ✅ Prevent multiple dots
        if obj.text == "." and "." in text:
            return

        # ✅ Leading dot fix
        if text == "" and obj.text == ".":
            self.active_input.text = "0."
            return

        self.active_input.text += obj.text

    def to_ft(self, ft, inch):
        try:
            return float(ft or 0) + float(inch or 0) / 12
        except:
            return 0.0

    def calculate(self, obj):
        self.vibrate(50)
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
        self.vibrate(60)
        for w in self.all_fields:
            w.text = ""
            w.line_color_normal = (0.5, 0.5, 0.5, 1)

        self.result.text = "0.00"
        self.active_input = None


if __name__ == "__main__":
    LumberApp().run()
