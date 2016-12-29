from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class DSBox(QtGui.QDoubleSpinBox):
    def __init__(self, foo):
        super(DSBox, self).__init__()
        self.foo = foo
        self.setRange(-999999999.99, 999999999.99)
        self.valueChanged.connect(self.foo)
        self.setMaximumWidth(80)


class FloatNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(FloatNode, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.spin_box = DSBox(self.set_data)
        self.graph = graph
        self.layout.setSpacing(3)
        self.output = self._add_port(AGPortTypes.kOutput, AGPortDataTypes.tNumeric, 'out')

        # hack! overload the output's port 'set_data' method to update lineEdit
        def set_data_overloads(data, dirty_propagate=True):
            self.spin_box.setValue(float(data))
        self.output.set_data_overload = set_data_overloads

        spin_box_proxy = QtGui.QGraphicsProxyWidget()
        spin_box_proxy.setWidget(self.spin_box)
        self.output.getLayout().insertItem(0, spin_box_proxy)
        self.compute()

    @staticmethod
    def get_category():
        return 'GenericTypes'

    def set_data(self):

        self.output.set_data(self.spin_box.value(), True)

    def compute(self):

        self.output.set_data(self.spin_box.value(), False)
