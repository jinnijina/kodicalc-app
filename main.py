from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


class LumberApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        screen = Screen()

        main = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )

        # ================= HEADER (ANDROID STYLE) =================
        header = MDBoxLayout(
            size_hint=(1, None),
            height=dp(65),
            padding=dp(10),
            md_bg_color=self.theme_cls.primary_color  # matches theme green
        )

        header.add_widget(MDLabel(
            text="Lumber Kodi Calculator",
            halign="center",
            valign="middle",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  # white text for contrast
        ))
        main.add_widget(header)

        # ================= RESULT CARD (COLORFUL) =================
        self.result = MDLabel(
            text="Ready to calculate",
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )

        result_card = MDBoxLayout(
            padding=dp(15),
            size_hint=(1, None),
            height=dp(90),
            md_bg_color=(0.1, 0.6, 0.3, 1),  # GREEN CARD
            radius=[15, 15, 15, 15]
        )

        result_card.add_widget(self.result)
        main.add_widget(result_card)

        # ================= INPUT ROW FUNCTION =================
        def row(label, ft_hint, in_hint):
            row_box = MDBoxLayout(
                spacing=dp(10),
                size_hint=(1, None),
                height=dp(55)
            )

            row_box.add_widget(MDLabel(
                text=label,
                size_hint=(0.3, 1)
            ))

            ft = MDTextField(
                hint_text=ft_hint,
                mode="rectangle",
                size_hint=(0.35, 1)
            )

            inch = MDTextField(
                hint_text=in_hint,
                mode="rectangle",
                size_hint=(0.35, 1)
            )

            row_box.add_widget(ft)
            row_box.add_widget(inch)

            return row_box, ft, inch

        # ================= INPUTS (ROW STYLE) =================
        self.len_row, self.len_ft, self.len_in = row("Length", "ft", "inch")
        self.wid_row, self.wid_ft, self.wid_in = row("Width", "ft", "inch")
        self.hei_row, self.hei_ft, self.hei_in = row("Height", "ft", "inch")

        main.add_widget(self.len_row)
        main.add_widget(self.wid_row)
        main.add_widget(self.hei_row)

        # ================= EXTRA INPUTS =================
        self.qty = MDTextField(hint_text="Quantity", mode="rectangle")
        self.rate = MDTextField(hint_text="Rate per ft³", mode="rectangle")

        main.add_widget(self.qty)
        main.add_widget(self.rate)

        # ================= BUTTONS =================
        btn_box = MDBoxLayout(
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(50)
        )

        btn_calc = MDRaisedButton(
            text="CALCULATE",
            on_release=self.calculate
        )

        btn_clear = MDFlatButton(
            text="CLEAR",
            on_release=self.clear
        )

        btn_box.add_widget(btn_calc)
        btn_box.add_widget(btn_clear)

        main.add_widget(btn_box)

        screen.add_widget(main)
        return screen

    # ================= CONVERT =================
    def to_ft(self, ft, inch):
        return float(ft or 0) + float(inch or 0) / 12

    # ================= CALCULATE =================
    def calculate(self, obj):
        try:
            L = self.to_ft(self.len_ft.text, self.len_in.text)
            W = self.to_ft(self.wid_ft.text, self.wid_in.text)
            H = self.to_ft(self.hei_ft.text, self.hei_in.text)

            qty = int(self.qty.text or 1)
            rate = float(self.rate.text or 0)

            volume = L * W * H * qty
            total = volume * rate

            # 🌈 colorful result
            self.result.text = (
                f"Kodi:  {volume:.2f} ft³\n"
                f"Total: {total:.2f}/-"
            )

        except:
            self.result.text = "Error ❌ Check input"

    # ================= CLEAR =================
    def clear(self, obj):
        for w in [
            self.len_ft, self.len_in,
            self.wid_ft, self.wid_in,
            self.hei_ft, self.hei_in,
            self.qty, self.rate
        ]:
            w.text = ""

        self.result.text = "Ready to calculate"


if __name__ == "__main__":
    LumberApp().run()