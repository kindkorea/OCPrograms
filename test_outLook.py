from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

class DragOutWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QListWidget.SingleSelection)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setUrls([Qt.QUrl.fromLocalFile(item.text())])  # 파일 경로 전달
        drag.setMimeData(mime_data)

        drag.exec_(Qt.CopyAction)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("드래그 아웃 데모")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)
        self.listWidget = DragOutWidget()
        layout.addWidget(self.listWidget)

        # 예제 파일 경로 추가
        self.listWidget.addItem(QListWidgetItem("C:/Users/kindk/OneDrive/OCWOOD_OFFICE/005_셈플사진/도어/예림_방화문.pdf"))
        self.listWidget.addItem(QListWidgetItem("./fax_receive/Travel_photo.srt"))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
