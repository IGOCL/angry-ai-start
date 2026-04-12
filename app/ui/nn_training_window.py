from __future__ import annotations

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout
import pyqtgraph as pg


class NNTrainingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neural Network Training")
        self.resize(1080, 760)

        self.loss_x = []
        self.loss_y = []
        self.acc_x = []
        self.acc_y = []
        self.current_generation = 0
        self.candidate_note = "waiting..."

        layout = QVBoxLayout(self)
        self.arch_label = QLabel("Architecture: waiting...")
        self.arch_label.setStyleSheet("font-size:15px; font-weight:700;")
        self.status_label = QLabel("Pipeline generation: waiting...")
        self.status_label.setStyleSheet("color:#8fb0d4; font-size:13px;")

        chip_row = QHBoxLayout()
        self.loss_chip = QLabel("Latest loss: -")
        self.acc_chip = QLabel("Latest acc: -")
        self.epoch_chip = QLabel("Epoch: -")
        for chip in (self.loss_chip, self.acc_chip, self.epoch_chip):
            chip.setStyleSheet("padding:4px 8px; border:1px solid #2a3d56; border-radius:10px;")
            chip_row.addWidget(chip)
        chip_row.addStretch(1)

        self.topology_plot = pg.PlotWidget(title="NN Topology")
        self.topology_plot.setMouseEnabled(x=False, y=False)
        self.topology_plot.hideAxis("left")
        self.topology_plot.hideAxis("bottom")
        self.topology_plot.setYRange(-1, 1)

        self.loss_plot = pg.PlotWidget(title="NN Loss")
        self.loss_plot.setLabel("left", "Loss")
        self.loss_plot.setLabel("bottom", "Epoch")

        self.acc_plot = pg.PlotWidget(title="NN Accuracy")
        self.acc_plot.setLabel("left", "Accuracy")
        self.acc_plot.setLabel("bottom", "Epoch")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        layout.addWidget(self.arch_label)
        layout.addWidget(self.status_label)
        layout.addLayout(chip_row)
        layout.addWidget(self.topology_plot, 2)
        layout.addWidget(self.loss_plot, 2)
        layout.addWidget(self.acc_plot, 2)
        layout.addWidget(self.log_box, 2)

    def set_architecture(self, text: str):
        self.arch_label.setText(f"Architecture: {text}")
        self._draw_topology(text)

    def on_generation(self, gen: int, survivors: int, population: int):
        self.current_generation = int(gen)
        self.status_label.setText(
            f"Pipeline generation: {gen} | survivors={survivors} | population={population} | candidate={self.candidate_note}"
        )

    def on_candidate(self, gen: int, done: int, total: int, family: str):
        self.candidate_note = f"{family} {done}/{total}"
        if self.current_generation <= 0:
            self.current_generation = int(gen)
        self.status_label.setText(
            f"Pipeline generation: {self.current_generation} | candidate={family} {done}/{total}"
        )

    def on_epoch(self, epoch: int, total: int, loss: float, acc: float):
        self.loss_x.append(epoch)
        self.loss_y.append(loss)
        self.acc_x.append(epoch)
        self.acc_y.append(acc)

        self.loss_plot.clear()
        self.acc_plot.clear()
        self.loss_plot.plot(self.loss_x, self.loss_y, pen=pg.mkPen("#ff6b6b", width=2))
        self.acc_plot.plot(self.acc_x, self.acc_y, pen=pg.mkPen("#00d4ff", width=2))
        self.loss_chip.setText(f"Latest loss: {loss:.5f}")
        self.acc_chip.setText(f"Latest acc: {acc:.4f}")
        self.epoch_chip.setText(f"Epoch: {epoch}/{total}")
        self.log_box.append(f"Epoch {epoch}/{total} | loss={loss:.5f} | acc={acc:.4f}")

    def on_finished(self):
        self.log_box.append("Training complete.")

    def _draw_topology(self, arch: str):
        self.topology_plot.clear()
        if not arch:
            return
        layer_sizes: list[int] = []
        for part in [x.strip() for x in arch.split("->")]:
            if "(" not in part or ")" not in part:
                continue
            try:
                val = int(part.split("(", 1)[1].split(")", 1)[0].split(",")[0].strip())
                layer_sizes.append(max(1, min(14, val)))
            except Exception:
                continue
        if len(layer_sizes) < 2:
            return

        x_step = 1.0 / max(1, len(layer_sizes) - 1)
        layer_points: list[list[tuple[float, float]]] = []
        for idx, size in enumerate(layer_sizes):
            x = idx * x_step
            ys = [0.0] if size == 1 else [1 - (2 * i / (size - 1)) for i in range(size)]
            points = [(x, y * 0.8) for y in ys]
            layer_points.append(points)

        for i in range(len(layer_points) - 1):
            left = layer_points[i]
            right = layer_points[i + 1]
            for x1, y1 in left:
                for x2, y2 in right:
                    self.topology_plot.plot(
                        [x1, x2],
                        [y1, y2],
                        pen=pg.mkPen(color=(70, 110, 160, 90), width=1),
                    )
        for pts in layer_points:
            x = [p[0] for p in pts]
            y = [p[1] for p in pts]
            self.topology_plot.plot(
                x,
                y,
                pen=None,
                symbol="o",
                symbolSize=9,
                symbolBrush=(130, 220, 255, 220),
                symbolPen=pg.mkPen("#63d8ff", width=1),
            )
