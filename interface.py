import tkinter as tk
import customtkinter

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # configure window
        self.title("Sweatbox Scenario Generator")
        self.geometry(f"{1100}x{580}")

        self.vfrPercentage = tk.IntVar()
        self.invalidRoutePercentage = tk.IntVar()
        self.invalidLevelPercentage = tk.IntVar()
        self.fplanErrorsPercentage = tk.IntVar()

        self.placeSliders()

    def placeSliders(self):

        # VFR Traffic
        self.vfrLabel = customtkinter.CTkLabel(
            self, text=f"Percentage of VFR Aircraft: 0%", fg_color="transparent", justify="left")
        self.vfrLabel.grid(row=2, column=0, padx=20, pady=20)

        vfrSlider = customtkinter.CTkSlider(
            self, from_=0, to=100, variable=self.vfrPercentage, command=self.updateVFRLabel)
        vfrSlider.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Invalid Routes
        self.invalidRouteLabel = customtkinter.CTkLabel(
            self, text=f"Percentage of VFR Aircraft: 0%", fg_color="transparent", justify="left")
        self.invalidRouteLabel.grid(row=4, column=0, padx=20, pady=20)

        invalidRouteIFR = customtkinter.CTkSlider(
            self, from_=0, to=100, variable=self.invalidRoutePercentage, command=self.updateInvalidRouteLabel)
        invalidRouteIFR.grid(row=5, column=0, padx=20, pady=(0, 20))

        # Invalid Levels
        self.invalidLevelLabel = customtkinter.CTkLabel(
            self, text=f"Percentage of VFR Aircraft: 0%", fg_color="transparent", justify="left")
        self.invalidLevelLabel.grid(row=6, column=0, padx=20, pady=20)

        invalidLevelIFR = customtkinter.CTkSlider(
            self, from_=0, to=100, variable=self.invalidLevelPercentage, command=self.updateInvalidLevelLabel)
        invalidLevelIFR.grid(row=7, column=0, padx=20, pady=20)

        # General Flightplan Errors
        self.fplanErrorsLabel = customtkinter.CTkLabel(
            self, text=f"Percentage of VFR Aircraft: 0%", fg_color="transparent", justify="left")
        self.fplanErrorsLabel.grid(row=8, column=0, padx=20, pady=20)

        fplanErrors = customtkinter.CTkSlider(
            self, from_=0, to=100, variable=self.fplanErrorsPercentage, command=self.updateFplanErrorsLabel)
        fplanErrors.grid(row=9, column=0, padx=20, pady=20)

    def updateVFRLabel(self, value) -> None:
        self.vfrLabel.configure(
            text=f"Percentage of VFR Aircraft: {int(value)}%")

    def updateInvalidRouteLabel(self, value) -> None:
        self.invalidRouteLabel.configure(
            text=f"Percentage of Invalid Routes: {int(value)}%")

    def updateInvalidLevelLabel(self, value) -> None:
        self.invalidLevelLabel.configure(
            text=f"Percentage of Invalid Level: {int(value)}%")

    def updateFplanErrorsLabel(self, value) -> None:
        self.fplanErrorsLabel.configure(
            text=f"Percentage of Flightplan Errors: {int(value)}%")


if __name__ == "__main__":
    app = App()
    app.mainloop()
