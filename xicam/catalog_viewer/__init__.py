from qtpy.QtWidgets import QLabel, QComboBox, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView
import logging
from xicam.core import msg
# log = logging.getLogger('catalog_viewer')

class CatalogViewerBlend(XArrayView, CatalogView):

    def __init__(self, *args, **kwargs):
        # CatalogViewerBlend inherits methods from XArrayView and CatalogView
        # super allows us to access both methods when calling super() from Blend
        super(CatalogViewerBlend, self).__init__(*args, **kwargs)


class CatalogViewerPlugin(GUIPlugin):
    name = 'Catalog Viewer'
    def __init__(self):
        self.layout = QHBoxLayout()
        self.parent_widget = QWidget()
        # add combobox to select stream
        self.field_label_stream = QLabel('Select stream:')
        self.field_combo_box_stream = QComboBox()
        self.field_combo_box_stream.setFixedWidth(150)
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

        self.stages = {'Viewer': GUILayout(top=self.parent_widget, 
                       center=self.catalog_viewer), }
        super(CatalogViewerPlugin, self).__init__()

    def field_changed(self, new_device):
        try:
            self.catalog_viewer.fieldChanged(new_device)
        except Exception as e:
            msg.logError(e)

    def stream_changed(self, new_stream):
        try:
            self.catalog_viewer.streamChanged(new_stream)
        except Exception as e:
            msg.logError(e)

    def appendCatalog(self, run_catalog, **kwargs):
        try:
            msg.showMessage(f"Loading primary image for {run_catalog.name}")
            self.catalog_viewer.setCatalog(run_catalog, 'primary', None)
            all_fields = run_catalog.primary.metadata['descriptors'][0]['data_keys']
            image_fields = []
            for field, field_descriptor in all_fields.items():
                field_shape = len(field_descriptor['shape'])
                if field_shape > 1 and field_shape < 5:
                    # if field contains at least 1 entry that is at least one-dimensional (shape=2) 
                    # or 2-dimensional (shape=3) or up to 3-dimensional (shape=4)
                    # then add field e.g. 'fccd_image'
                    image_fields.append(field)

            stream_fields = []
            for stream in list(run_catalog):
                # check if image_field exists in different streams
                # if yes -> add to stream_fields -> can be selected in CatalogViewer select_stream
                if image_fields[0] in run_catalog[stream].metadata['descriptors'][0]['data_keys']:
                    stream_fields.append(stream)
                else:
                    msg.showMessage("{0} stream does not contain {1} image data".format(stream, image_fields[0]))
                #ToDo:
                # Handle multiple image fields per stream
                # Where/how to display non 2D stream fields --> such as metadata?

            self.field_combo_box.clear()
            self.field_combo_box.addItems(image_fields)
            self.field_combo_box_stream.clear()
            self.field_combo_box_stream.addItems(stream_fields)
        except Exception as e:
            msg.logError(e)
            msg.showMessage("Unable to display: ", str(e))

    def appendHeader(self):
        ...
