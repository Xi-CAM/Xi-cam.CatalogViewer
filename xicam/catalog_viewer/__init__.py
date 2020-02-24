from qtpy.QtWidgets import QLabel, QComboBox, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView
from xicam.gui.bluesky.summary import SummaryWidget
import logging

log = logging.getLogger('catalog_viewer')

class CatalogViewerBlend(XArrayView, CatalogView):

    def __init__(self, *args, **kwargs):
        #Q: CatalogViewerBlend inherits methods from XArrayView and CatalogView
        # --> Therefore super allows us to access both methods when calling super() from Blend
        super(CatalogViewerBlend, self).__init__(*args, **kwargs)


class CatalogViewerPlugin(GUIPlugin):
    name = 'Catalog Viewer'
    def __init__(self):
        self.layout = QHBoxLayout()
        self.parent_widget = QWidget()
        # add combobox to select stream
        self.field_label_stream = QLabel('Select stream:')
        self.field_combo_box_stream = QComboBox()
        self.field_combo_box_stream.setFixedWidth(120)
        self.layout.addWidget(self.field_label_stream)
        self.layout.addWidget(self.field_combo_box_stream)
        self.field_combo_box_stream.currentTextChanged.connect(self.stream_changed)
        # add combobox to select image in stream
        self.field_label = QLabel('Select image:')
        self.field_combo_box = QComboBox()
        self.field_combo_box.setFixedWidth(150)
        self.layout.addWidget(self.field_label)
        self.layout.addWidget(self.field_combo_box)
        self.field_combo_box.currentTextChanged.connect(self.field_changed)

        self.layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.parent_widget.setLayout(self.layout)
        self.catalog_viewer = CatalogViewerBlend()
        # self.stream_viewer = SummaryWidget()
        self.stages = {'Viewer': GUILayout(top=self.parent_widget, 
                       center=self.catalog_viewer), }
        super(CatalogViewerPlugin, self).__init__()

    def field_changed(self, new_device):
        try:
            self.catalog_viewer.fieldChanged(new_device)
        except Exception as e:
            log.error(e)

    def stream_changed(self, new_stream):
        try:
            self.catalog_viewer.streamChanged(new_stream)
        except Exception as e:
            log.error(e)

    def appendCatalog(self, run_catalog, **kwargs):
        try:
            msg.showMessage(f"Loading primary image for {run_catalog.name}")
            self.catalog_viewer.setCatalog(run_catalog, 'primary', None)
            stream_fields = run_catalog.primary.metadata['stop']['num_events'].keys() or {}
            all_fields = run_catalog.primary.metadata['descriptors'][0]['data_keys']
            image_fields = []
            for field, field_descriptor in all_fields.items():
                field_shape = len(field_descriptor['shape'])
                if field_shape > 1 and field_shape < 5:
                    image_fields.append(field)
            self.field_combo_box.clear()
            self.field_combo_box.addItems(image_fields)
            self.field_combo_box_stream.clear()
            self.field_combo_box_stream.addItems(stream_fields)
        except Exception as e:
            log.error(e)
            msg.showMessage("Unable to display: ", str(e))

    def appendHeader(self):
        ...
