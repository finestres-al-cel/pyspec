""" Functions to load Actions"""
from PyQt6.QtGui import QAction, QIcon

from pyspec.app.environment import BUTTONS_PATH

def loadMainActions(window):
    """Load main menu actions

    Arguments
    ---------
    window: MainWindow
    Window where the actions will act

    Return
    ------
    menuAction: list of QAction
    List of actions in the main menu
    """
    menuActions = []

    load_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/load_image.png"),
        "&Load Spectrum",
        window)
    load_spectrum_option.setStatusTip("Load Spectrum")
    load_spectrum_option.triggered.connect(window.open_file)
    menuActions.append(load_spectrum_option)

    extract_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
        "&Extract Spectrum",
        window)
    extract_spectrum_option.setStatusTip("Extract Spectrum")
    extract_spectrum_option.triggered.connect(window.onMyToolBarButtonClick)
    extract_spectrum_option.setCheckable(True)
    menuActions.append(extract_spectrum_option)

    plot_raw_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/plot_spec.png"),
        "&Plot Spectrum",
        window)
    plot_raw_spectrum_option.setStatusTip("Plot Spectrum")
    plot_raw_spectrum_option.triggered.connect(window.onMyToolBarButtonClick)
    plot_raw_spectrum_option.setCheckable(True)
    menuActions.append(plot_raw_spectrum_option)

    set_calibration_option = QAction(
        QIcon(f"{BUTTONS_PATH}/set_calib.png"),
        "&Set Calibration",
        window)
    set_calibration_option.setStatusTip("Set Calibration")
    set_calibration_option.triggered.connect(window.onMyToolBarButtonClick)
    set_calibration_option.setCheckable(True)
    menuActions.append(set_calibration_option)

    load_calibration_option = QAction(
        QIcon(f"{BUTTONS_PATH}/load_calib.png"),
        "&Load Calibration",
        window)
    load_calibration_option.setStatusTip("Load Calibration")
    load_calibration_option.triggered.connect(window.onMyToolBarButtonClick)
    load_calibration_option.setCheckable(True)
    menuActions.append(load_calibration_option)

    return menuActions
