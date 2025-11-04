#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Geracao de sinal a partir de sua serie de Fourier
# Author: Leocarlos Bezerra da Silva Lima
# Description: Experimento para Laboratório de Princípios de Comunicações. Departamento de Engenharia Elétrica - DEE da Universidade Federal de Campina Grande - UFCG.
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class Labo1_2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Geracao de sinal a partir de sua serie de Fourier", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Geracao de sinal a partir de sua serie de Fourier")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Labo1_2")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8000
        self.f0 = f0 = 0
        self.A3 = A3 = 0
        self.A2 = A2 = 0
        self.A1 = A1 = 0

        ##################################################
        # Blocks
        ##################################################

        self.Tab = Qt.QTabWidget()
        self.Tab_widget_0 = Qt.QWidget()
        self.Tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Tab_widget_0)
        self.Tab_grid_layout_0 = Qt.QGridLayout()
        self.Tab_layout_0.addLayout(self.Tab_grid_layout_0)
        self.Tab.addTab(self.Tab_widget_0, 'Amplitudes')
        self.Tab_widget_1 = Qt.QWidget()
        self.Tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Tab_widget_1)
        self.Tab_grid_layout_1 = Qt.QGridLayout()
        self.Tab_layout_1.addLayout(self.Tab_grid_layout_1)
        self.Tab.addTab(self.Tab_widget_1, 'Frequencia')
        self.top_grid_layout.addWidget(self.Tab, 4, 0, 2, 2)
        for r in range(4, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._f0_range = qtgui.Range(0, 1500, 50, 0, 200)
        self._f0_win = qtgui.RangeWidget(self._f0_range, self.set_f0, "fundamental", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Tab_grid_layout_1.addWidget(self._f0_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.Tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Tab_grid_layout_1.setColumnStretch(c, 1)
        self._A3_range = qtgui.Range(-1.5, 1.5, 0.01, 0, 200)
        self._A3_win = qtgui.RangeWidget(self._A3_range, self.set_A3, "Amplitude 3", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Tab_grid_layout_0.addWidget(self._A3_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.Tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Tab_grid_layout_0.setColumnStretch(c, 1)
        self._A2_range = qtgui.Range(-1.5, 1.5, 0.01, 0, 200)
        self._A2_win = qtgui.RangeWidget(self._A2_range, self.set_A2, "Amplitude 2", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Tab_grid_layout_0.addWidget(self._A2_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.Tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Tab_grid_layout_0.setColumnStretch(c, 1)
        self._A1_range = qtgui.Range(-1.5, 1.5, 0.01, 0, 200)
        self._A1_win = qtgui.RangeWidget(self._A1_range, self.set_A1, "Amplitude 1", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Tab_grid_layout_0.addWidget(self._A1_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.Tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Tab_grid_layout_0.setColumnStretch(c, 1)
        self.somador_0 = blocks.add_vff(1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.harmonica_2 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, (5*f0), A3, 0, 0)
        self.harmonica_1 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, (3*f0), A2, 0, 0)
        self.graf_tempo_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.graf_tempo_0.set_update_time(0.10)
        self.graf_tempo_0.set_y_axis(-1, 1)

        self.graf_tempo_0.set_y_label('Amplitude', "")

        self.graf_tempo_0.enable_tags(True)
        self.graf_tempo_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.graf_tempo_0.enable_autoscale(True)
        self.graf_tempo_0.enable_grid(True)
        self.graf_tempo_0.enable_axis_labels(True)
        self.graf_tempo_0.enable_control_panel(False)
        self.graf_tempo_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.graf_tempo_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.graf_tempo_0.set_line_label(i, labels[i])
            self.graf_tempo_0.set_line_width(i, widths[i])
            self.graf_tempo_0.set_line_color(i, colors[i])
            self.graf_tempo_0.set_line_style(i, styles[i])
            self.graf_tempo_0.set_line_marker(i, markers[i])
            self.graf_tempo_0.set_line_alpha(i, alphas[i])

        self._graf_tempo_0_win = sip.wrapinstance(self.graf_tempo_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._graf_tempo_0_win)
        self.fundamental = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, f0, A1, 0, 0)
        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.somador_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.somador_0, 2))
        self.connect((self.blocks_throttle_0_1, 0), (self.somador_0, 1))
        self.connect((self.fundamental, 0), (self.blocks_throttle_0, 0))
        self.connect((self.harmonica_1, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.harmonica_2, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.somador_0, 0), (self.graf_tempo_0, 0))
        self.connect((self.somador_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Labo1_2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_1.set_sample_rate(self.samp_rate)
        self.fundamental.set_sampling_freq(self.samp_rate)
        self.graf_tempo_0.set_samp_rate(self.samp_rate)
        self.harmonica_1.set_sampling_freq(self.samp_rate)
        self.harmonica_2.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.fundamental.set_frequency(self.f0)
        self.harmonica_1.set_frequency((3*self.f0))
        self.harmonica_2.set_frequency((5*self.f0))

    def get_A3(self):
        return self.A3

    def set_A3(self, A3):
        self.A3 = A3
        self.harmonica_2.set_amplitude(self.A3)

    def get_A2(self):
        return self.A2

    def set_A2(self, A2):
        self.A2 = A2
        self.harmonica_1.set_amplitude(self.A2)

    def get_A1(self):
        return self.A1

    def set_A1(self, A1):
        self.A1 = A1
        self.fundamental.set_amplitude(self.A1)




def main(top_block_cls=Labo1_2, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
