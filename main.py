from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.application.app import PdfToolkitApplication
from app.config.constants import APP_NAME, APP_ORGANIZATION, APP_VERSION


def main() -> int:
    qt_app = QApplication(sys.argv)

    qt_app.setApplicationName(APP_NAME)
    qt_app.setApplicationVersion(APP_VERSION)
    qt_app.setOrganizationName(APP_ORGANIZATION)

    application = PdfToolkitApplication(qt_app)
    application.initialize()

    qt_app.aboutToQuit.connect(application.shutdown)

    return application.run()


if __name__ == "__main__":
    raise SystemExit(main())
