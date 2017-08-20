#!/usr/bin/env python2
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('freqMHz',help='frequency in MHz to center on',nargs='+',type=float)
p = p.parse_args()



F = [int(f*1e6) for f in p.freqMHz]
Fs = int(192e3)
Fsink0 = 0 # display center freq

NRX = len(F) 
FTX = 0

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
import hpsdr
import sip
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Blocks
        ##################################################
        self.fsink0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	Fsink0, #fc
        	Fs, #bw
        	"", #name
        	2 #number of inputs
        )
        self.fsink0.set_update_time(0.10)
        self.fsink0.set_y_axis(-140, -10)
        self.fsink0.set_y_label('RX Level', 'dB')
        self.fsink0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.fsink0.enable_autoscale(False)
        self.fsink0.enable_grid(True)
        self.fsink0.set_fft_average(1.0)
        self.fsink0.enable_axis_labels(True)
        self.fsink0.enable_control_panel(True)
        
        if not True:
          self.fsink0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.fsink0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in range(2):
            if len(labels[i]) == 0:
                self.fsink0.set_line_label(i, "Data {0}".format(i))
            else:
                self.fsink0.set_line_label(i, labels[i])
            self.fsink0.set_line_width(i, widths[i])
            self.fsink0.set_line_color(i, colors[i])
            self.fsink0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.fsink0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        
        self.hpsdr_hermesNB_0 = hpsdr.hermesNB(RxFreq0=F[0], RxFreq1=F[1],
                                               TxFreq=FTX, 
                                               RxPre=False, PTTModeSel=0, PTTTxMute=True, PTTRxMute=True, TxDr=0, 
                                               RxSmp=Fs, Intfc="enp0s25", ClkS="0xF8", 
                                               AlexRA=0, AlexTA=0, AlexHPF=0x00, AlexLPF=0x00, Verbose=0, 
                                               NumRx=NRX,MACAddr="*")
        self.dummytx = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
# %% Connections
        self.connect((self.dummytx, 0), (self.hpsdr_hermesNB_0, 0))   
        
        self.connect((self.hpsdr_hermesNB_0, 0), (self.fsink0, 0)) 
        self.connect((self.hpsdr_hermesNB_0, 1), (self.fsink0, 1))
        self.connect((self.hpsdr_hermesNB_0, 2), (self.fsink0, 2))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()