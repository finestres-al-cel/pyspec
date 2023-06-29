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
    load_spectrum_option.triggered.connect(window.openFile)
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
    extract_spectrum_option.triggered.connect(window.extractSpectrum)
    extract_spectrum_option.setCheckable(True)
    extract_spectrum_option.setEnabled(False)
    menuActions.append(extract_spectrum_option)

    rotate_image_option = QAction(
        QIcon(f"{BUTTONS_PATH}/rotate.png"),
        "&Rotate Image",
        window)
    rotate_image_option.setStatusTip("Rotate Image")
    rotate_image_option.triggered.connect(window.rotateImage)
    rotate_image_option.setEnabled(False)
    menuActions.append(rotate_image_option)

    set_upper_limit_option = QAction(
        QIcon(f"{BUTTONS_PATH}/upper_lim.png"),
        "Set &Upper Limit",
        window)
    set_upper_limit_option.setStatusTip("Set Upper Limit")
    set_upper_limit_option.triggered.connect(
        lambda checked: window.activateChooseLimitOnClick(
            checked, set_upper_limit_option))
    set_upper_limit_option.setCheckable(True)
    set_upper_limit_option.setEnabled(False)
    menuActions.append(set_upper_limit_option)

    set_lower_limit_option = QAction(
        QIcon(f"{BUTTONS_PATH}/lower_lim.png"),
        "Set &Lower Limit",
        window)
    set_lower_limit_option.setStatusTip("Set Lower Limit")
    set_lower_limit_option.triggered.connect(
        lambda checked: window.activateChooseLimitOnClick(
            checked, set_lower_limit_option))
    set_lower_limit_option.setCheckable(True)
    set_lower_limit_option.setEnabled(False)
    menuActions.append(set_lower_limit_option)

    return menuActions

def loadSpectrumActions(window):
    """Load spectrum menu actions

    Arguments
    ---------
    window: MainWindow
    Window where the actions will act

    Return
    ------
    menuAction: list of QAction
    List of actions in the spectrum menu
    """
    menuActions = []

    save_spectrum_option = QAction(
        QIcon(f"{BUTTONS_PATH}/save.png"),
        "&Save Spectrum",
        window)
    save_spectrum_option.setStatusTip("Save Spectrum")
    save_spectrum_option.triggered.connect(window.saveSpectrum)
    save_spectrum_option.setEnabled(False)
    menuActions.append(save_spectrum_option)

    set_calibration_option = QAction(
        QIcon(f"{BUTTONS_PATH}/set_calib.png"),
        "&Set Calibration",
        window)
    set_calibration_option.setStatusTip("Set Calibration")
    set_calibration_option.triggered.connect(window.onMyToolBarButtonClick)
    set_calibration_option.setCheckable(True)
    set_calibration_option.setEnabled(False)
    menuActions.append(set_calibration_option)

    load_calibration_option = QAction(
        QIcon(f"{BUTTONS_PATH}/load_calib.png"),
        "&Load Calibration",
        window)
    load_calibration_option.setStatusTip("Load Calibration")
    load_calibration_option.triggered.connect(window.onMyToolBarButtonClick)
    load_calibration_option.setCheckable(True)
    load_calibration_option.setEnabled(False)
    menuActions.append(load_calibration_option)

    return menuActions
