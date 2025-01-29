import tkinter as tk
from tkinter import filedialog
import customtkinter
import os
import re
from utils import generateSweatboxText


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_appearance_mode("Dark")
        # Themes: "blue" (standard), "green", "dark-blue"
        customtkinter.set_default_color_theme("green")

        self.vfrPercentage = tk.IntVar()
        self.invalidRoutePercentage = tk.IntVar()
        self.invalidLevelPercentage = tk.IntVar()
        self.fplanErrorsPercentage = tk.IntVar()
        self.numberOfPlanes = tk.StringVar(value=20)

        self.sectorFileLocation = None
        self.outputDirectory = None

        # configure window
        self.title("Sweatbox Scenario Generator")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0, minsize=240)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.airportSelectFrame = customtkinter.CTkFrame(
            self, corner_radius=12)
        self.airportSelectFrame.grid(
            row=0, column=0, rowspan=4, sticky="nsew", padx=5, pady=5)
        self.airportSelectFrame.grid_rowconfigure(3, weight=1)
        self.airportSelectFrame.grid_columnconfigure(0, weight=1)

        airportSelectLabel = customtkinter.CTkLabel(
            self.airportSelectFrame, text="Select Airport", font=customtkinter.CTkFont(size=20, weight="bold"))
        airportSelectLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.placeAirportSelect()

        self.configFrame = customtkinter.CTkFrame(
            self, corner_radius=12)
        self.configFrame.grid(row=0, column=1, rowspan=4,
                              columnspan=1, sticky="nsew", padx=5, pady=5)

        self.placeSliders()

        self.summaryFrame = customtkinter.CTkFrame(
            self, corner_radius=12)
        self.summaryFrame.grid(row=0, column=2, rowspan=3,
                               sticky="nsew", padx=5, pady=5)
        self.summaryFrame.grid_columnconfigure(0, weight=1)
        self.summaryFrame.grid_rowconfigure(4, weight=1)

        customtkinter.CTkLabel(self.summaryFrame, text="Summary",
                               font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=0, pady=(20, 10))

        self.generateFrame = customtkinter.CTkFrame(
            self, corner_radius=12)
        self.generateFrame.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)
        self.generateFrame.grid_columnconfigure(0, weight=1)
        self.generateFrame.grid_rowconfigure(2, weight=1)

        customtkinter.CTkLabel(self.generateFrame, text="Number of Planes",
                               fg_color="transparent").grid(row=0, column=0, padx=20, pady=(10, 5))

        self.entry = customtkinter.CTkEntry(
            self.generateFrame, placeholder_text=self.numberOfPlanes.get())
        self.entry.grid(row=1, column=0, padx=20, pady=(5, 10))

        self.manualAdd = customtkinter.CTkButton(
            self.generateFrame, text="Add Pilot Manually", command=self.addManualPilot)
        self.manualAdd.grid(row=2, column=0, padx=20, pady=10)

        self.generateButton = customtkinter.CTkButton(
            self.generateFrame, text="Generate Sweatbox file", command=self.generate)
        self.generateButton.grid(row=3, column=0, padx=20, pady=10)

    def placeSliders(self) -> None:

        # VFR Traffic
        self.vfrLabel = customtkinter.CTkLabel(
            self.configFrame, text=f"Percentage of VFR Aircraft: 0%", fg_color="transparent", justify="left")
        self.vfrLabel.grid(row=2, column=0, padx=20, pady=20)

        vfrSlider = customtkinter.CTkSlider(
            self.configFrame, from_=0, to=100, variable=self.vfrPercentage, command=self.updateVFRLabel)
        vfrSlider.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Invalid Routes
        self.invalidRouteLabel = customtkinter.CTkLabel(
            self.configFrame, text=f"Percentage of Invalid Routes: 0%", fg_color="transparent", justify="left")
        self.invalidRouteLabel.grid(row=4, column=0, padx=20, pady=20)

        invalidRouteIFR = customtkinter.CTkSlider(
            self.configFrame, from_=0, to=100, variable=self.invalidRoutePercentage, command=self.updateInvalidRouteLabel)
        invalidRouteIFR.grid(row=5, column=0, padx=20, pady=(0, 20))

        # Invalid Levels
        self.invalidLevelLabel = customtkinter.CTkLabel(
            self.configFrame, text=f"Percentage of Invalid Level: 0%", fg_color="transparent", justify="left")
        self.invalidLevelLabel.grid(row=6, column=0, padx=20, pady=20)

        invalidLevelIFR = customtkinter.CTkSlider(
            self.configFrame, from_=0, to=100, variable=self.invalidLevelPercentage, command=self.updateInvalidLevelLabel)
        invalidLevelIFR.grid(row=7, column=0, padx=20, pady=20)

        # General Flightplan Errors
        self.fplanErrorsLabel = customtkinter.CTkLabel(
            self.configFrame, text=f"Percentage of Flightplan Errors: 0%", fg_color="transparent", justify="left")
        self.fplanErrorsLabel.grid(row=8, column=0, padx=20, pady=20)

        fplanErrors = customtkinter.CTkSlider(
            self.configFrame, from_=0, to=100, variable=self.fplanErrorsPercentage, command=self.updateFplanErrorsLabel)
        fplanErrors.grid(row=9, column=0, padx=20, pady=20)

    def placeAirportSelect(self) -> None:
        self.airportSelectButton = customtkinter.CTkButton(
            self.airportSelectFrame, text="EGPH", command=self.switchAirport)
        self.airportSelectButton.grid(row=1, column=0, padx=20, pady=(20, 20))

    def getSectorFile(self) -> str:
        if not self.sectorFileLocation:
            ukPack = self.selectDirectory("UK controller Pack")
            self.sectorFileLocation = f"{ukPack}/Data/Sector"
            self.writeOptions()
            sector_files = os.listdir(self.sectorFileLocation)
            pattern = re.compile(r"UK_\d{4}_\d{2}\.sct")

            for file in sector_files:
                if pattern.match(file):
                    sectorFilePath = os.path.join(
                        self.sectorFileLocation, file)
                    break

        with open(sectorFilePath, "r")as sf:
            ...  # process

    def loadOptions(self) -> None:
        if os.path.exists("sweatbox_generator.config"):
            with open("sweatbox_generator.config", "r") as configFile:
                config = configFile.read().split(',')
                if len(config) >= 2:
                    self.sectorFileLocation = config[0]
                    self.outputDirectory = config[1]

    def writeOptions(self) -> None:
        with open("sweatbox_generator.config", "w")as configFile:
            configFile.write(f"{self.sectorFileLocation},")
            configFile.write(f"{self.outputDirectory},")

    def selectDirectory(self, dir: str) -> str:
        return filedialog.askdirectory(title=f"Select {dir}")

    def generate(self) -> None:
        self.sweatboxContents = generateSweatboxText()
        if not self.outputDirectory:
            self.outputDirectory = self.selectDirectory("Output")
        self.writeOptions()
        with open(f"{self.outputDirectory}/sweatbox.txt", "w")as outFile:
            outFile.write(self.sweatboxContents)

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

    def switchAirport(self) -> None:
        ...

    def addManualPilot(self) -> None:
        ...


if __name__ == "__main__":
    app = App()
    app.mainloop()
