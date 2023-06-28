""" Functions to load Actions"""
from PyQt6.QtGui import QAction, QIcon

from pyspec.app.environment import BUTTONS_PATH

def loadFileMenuActions(window):
    """Load file menu actions

    Arguments
    ---------
    window: MainWindow
    Window where the actions will act

    Return
    ------
    menuAction: list of QAction
    List of actions in the file menu
    """
    menuActions = []

    load_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/load_image.png"),
        "&Load Spectrum",
        window)
    load_spectrum_option.setStatusTip("Load Spectrum")
    load_spectrum_option.triggered.connect(window.open_file)
    menuActions.append(load_spectrum_option)

    return menuActions

def loadSpectralExtractionActions(window):
    """Load spectral extraction menu actions

    Arguments
    ---------
    window: MainWindow
    Window where the actions will act

    Return
    ------
    menuAction: list of QAction
    List of actions in the spectral extraction menu
    """
    menuActions = []

    extract_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
        "&Extract Spectrum",
        window)
    extract_spectrum_option.setStatusTip("Extract Spectrum")
    extract_spectrum_option.triggered.connect(window.onMyToolBarButtonClick)
    extract_spectrum_option.setCheckable(True)
    extract_spectrum_option.setEnabled(False)
    menuActions.append(extract_spectrum_option)

    rotate_image_option = QAction(
        QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
        "&Rotate Image",
        window)
    rotate_image_option.setStatusTip("Rotate Image")
    rotate_image_option.triggered.connect(window.rotate_image)
    rotate_image_option.setEnabled(False)
    menuActions.append(rotate_image_option)

    set_bottom_limit_option = QAction(
        QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
        "Set &Bottom Limit",
        window)
    set_bottom_limit_option.setStatusTip("Set Bottom Limit")
    set_bottom_limit_option.triggered.connect(window.onMyToolBarButtonClick)
    set_bottom_limit_option.setCheckable(True)
    set_bottom_limit_option.setEnabled(False)
    menuActions.append(set_bottom_limit_option)

    set_top_limit_option = QAction(
        QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
        "Set &Top Limit",
        window)
    set_top_limit_option.setStatusTip("Set Upper Limit")
    set_top_limit_option.triggered.connect(window.onMyToolBarButtonClick)
    set_top_limit_option.setCheckable(True)
    set_top_limit_option.setEnabled(False)
    menuActions.append(set_top_limit_option)

    return menuActions


def loadOtherActions(window):
    """Load other menu actions

    Arguments
    ---------
    window: MainWindow
    Window where the actions will act

    Return
    ------
    menuAction: list of QAction
    List of actions in the other menu
    """
    menuActions = []

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
