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
        self.stream_label = QLabel('Select stream:')
        self.stream_combo_box = QComboBox()
        self.stream_combo_box.setFixedWidth(150)
        self.layout.addWidget(self.field_label_stream)
        self.layout.addWidget(self.stream_combo_box)
        self.stream_combo_box.currentTextChanged.connect(self.stream_changed)
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
        self.stream_fields = None  # list containing tuples of stream + field
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
        finally:
            fields = get_fields_for_stream(self.stream_fields, new_stream)
            self.field_combo_box.clear()
            self.field_combo_box.addItems(fields)

    def appendCatalog(self, run_catalog, **kwargs):
        try:
            self.stream_fields = get_all_image_fields(run_catalog)
            self.field_combo_box.clear()
            self.stream_combo_box.clear()
            msg.showMessage(f"Loading primary image for {run_catalog.name}")
            self.catalog_viewer.setCatalog(run_catalog, 'primary', None)
            # try and startup with primary catalog and whatever fields it has
            filtered_stream_fields = get_fields_for_stream(self.stream_fields, 'primary')
            self.stream_combo_box.clear()
            self.stream_combo_box.addItems(get_all_streams(run_catalog))
            self.field_combo_box.clear()
            self.field_combo_box.addItems(filtered_stream_fields)

        except Exception as e:
            msg.logError(e)
            msg.showMessage("Unable to display: ", str(e))

    def appendHeader(self):
        ...


def get_stream_data_keys(run_catalog, stream):
    return run_catalog[stream].metadata['descriptors'][0]['data_keys']


def get_fields_for_stream(stream_fields, stream):
    return [stream_field_tuple[1] for stream_field_tuple in stream_fields if stream_field_tuple[0] == stream]


def get_all_streams(run_catalog):
    return list(run_catalog)


def get_all_image_fields(run_catalog):
    all_image_fields = []
    for stream in get_all_streams(run_catalog):
        stream_fields = get_stream_data_keys(run_catalog, stream)
        field_names = stream_fields.keys()
        for field_name in field_names:
            field_shape = len(stream_fields[field_name]['shape'])
            if field_shape > 1 and field_shape < 5:
                # if field contains at least 1 entry that is at least one-dimensional (shape=2) 
                # or 2-dimensional (shape=3) or up to 3-dimensional (shape=4)
                # then add field e.g. 'fccd_image'
                stream_field = (stream, field_name)
                all_fields.append(stream_field)
    return all_fields
