import PySimpleGUI as sg
import integralaprox as ia
import ctypes
import platform


class IntegralApproximatorGUI:
    def __init__(self):
        self.make_dpi_aware()
        self.define_layout()
        self.window = sg.Window("Integral Approximator",
                                self.layout, element_justification='c',
                                size=(900, 500))
        self.event_loop()
        self.window.close()

    def define_layout(self):
        input_info_layout = [
            [sg.Text("Expression")],
            [sg.Text("Lower bound")],
            [sg.Text("Higher bound")],
            [sg.Text("N")]
        ]
        input_field_layout = [
            [sg.In(size=(25, 1), key="-EXPRESSION-")],
            [sg.In(size=(5, 1), key="-LOWERBOUND-")],
            [sg.In(size=(5, 1), key="-HIGHERBOUND-")],
            [sg.In(size=(5, 1), key="-N-")],
        ]
        input_column_layout = [
            [
                sg.Column(input_info_layout),
                sg.Column(input_field_layout)
            ],
        ]
        result_info_layout = [
            [sg.Text("Calc type", font=(16))],
            [sg.Text("Definite Integration")],
            [sg.Text("Trapezoidal Approximation")],
            [sg.Text("Midpoint Approximation")],
            [sg.Text("Simpson's Approximation")]
        ]
        results_values_layout = [
            [sg.Text("Result", font=(16))],
            [sg.Text(key="-DEFINITE-")],
            [sg.Text(key="-TRAPEZOIDAL-")],
            [sg.Text(key="-MIDPOINT-")],
            [sg.Text(key="-SIMPSON-")]
        ]
        results_error_layout = [
            [sg.Text("Error bounds", font=(16))],
            [sg.Text(key="-DEFINITE_ERROR-")],
            [sg.Text(key="-TRAPEZOIDAL_ERROR-")],
            [sg.Text(key="-MIDPOINT_ERROR-")],
            [sg.Text(key="-SIMPSON_ERROR-")]
        ]
        results_column_layout = [
            [
                sg.Column(result_info_layout),
                sg.Column(results_values_layout),
                sg.Column(results_error_layout)
            ]
        ]
        self.layout = [
            input_column_layout,
            [sg.Button("Calculate", key="-CALCULATE-",
                       enable_events=True, size=(20, 1))],
            [sg.Column(results_column_layout, key="-RESULTS-", visible=False)]
        ]

    def update_results(self, results):
        for key, value in results.items():
            self.window[key].update(str(value))

    def event_loop(self):
        while True:
            event, values = self.window.read()

            if event == "-CALCULATE-":
                try:
                    results, errors = self.calculate_results(values)
                    self.update_results(results, errors)
                    self.show_results()
                except:
                    sg.Popup("Invalid input, please try again", title="Error")

            elif event == sg.WIN_CLOSED:
                break

    def calculate_results(self, values):
        exp = values["-EXPRESSION-"]
        high = float(values["-HIGHERBOUND-"])
        low = float(values["-LOWERBOUND-"])
        n = int(values["-N-"])
        results = ia.IntegralApproximator(
            exp, low, high, n).calc_all()
        errors = ia.IntegralApproximator(
            exp, low, high, n).calc_error()
        return results, errors

    def update_results(self, results, errors):
        for key, value in results.items():
            if value is None:
                value = "N/A"
            else:
                value = round(value, 6)
            self.window[key].update(str(value))
        for key, value in errors.items():
            if value is None:
                value = "N/A"
            else:
                value = round(value, 6)
            self.window[key].update(str(value))

    def show_results(self):
        self.window["-RESULTS-"].update(visible=True)

    def make_dpi_aware(self):
        # Fix DPI scaling issues on Windows 8 and above
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
