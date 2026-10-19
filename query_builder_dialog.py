from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox
)


class QueryBuilderDialog(QDialog):

    def __init__(self, iface):
        super().__init__()

        self.iface = iface

        self.setWindowTitle(
            "Query Builder"
        )

        self.resize(600, 450)

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Field")
        )

        self.field_combo = QComboBox()
        layout.addWidget(
            self.field_combo
        )

        layout.addWidget(
            QLabel("Operator")
        )

        self.operator_combo = QComboBox()

        self.operator_combo.addItems([
            "=",
            "!=",
            ">",
            "<",
            ">=",
            "<=",
            "LIKE",
            "IN"
        ])

        layout.addWidget(
            self.operator_combo
        )

        layout.addWidget(
            QLabel("Value(s)")
        )

        self.values_text = QTextEdit()
        layout.addWidget(
            self.values_text
        )

        self.expression_text = QTextEdit()
        layout.addWidget(
            self.expression_text
        )

        self.build_btn = QPushButton(
            "Build Expression"
        )

        self.build_btn.clicked.connect(
            self.build_expression
        )

        layout.addWidget(
            self.build_btn
        )

        self.select_btn = QPushButton(
            "Select Features"
        )

        self.select_btn.clicked.connect(
            self.select_features
        )

        layout.addWidget(
            self.select_btn
        )

        self.setLayout(layout)

        self.load_fields()

    def active_layer(self):

        return self.iface.activeLayer()

    def load_fields(self):

        layer = self.active_layer()

        if not layer:
            return

        self.field_combo.clear()

        for field in layer.fields():
            self.field_combo.addItem(
                field.name()
            )

    def build_expression(self):

        field = self.field_combo.currentText()
        op = self.operator_combo.currentText()

        values = self.values_text.toPlainText().strip()

        if not field:
            return

        if op == "IN":

            value_list = [
                v.strip()
                for v in values.split(",")
                if v.strip()
            ]

            quoted = ",".join(
                [f"'{v}'" for v in value_list]
            )

            expression = (
                f'"{field}" IN ({quoted})'
            )

        else:

            expression = (
                f'"{field}" {op} \'{values}\''
            )

        self.expression_text.setText(
            expression
        )

    def select_features(self):

        layer = self.active_layer()

        if not layer:
            QMessageBox.warning(
                self,
                "Error",
                "No active layer."
            )
            return

        expression = self.expression_text.toPlainText()

        if not expression:
            return

        layer.selectByExpression(
            expression
        )

        QMessageBox.information(
            self,
            "Done",
            f"Expression Applied:\n{expression}"
        )
