from qtpy.QtWidgets import QLabel, QComboBox, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qtpy.QtCore import Qt
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView


class CatalogViewerBlend(XArrayView, CatalogView):

    def __init__(self, *args, **kwargs):
        super(CatalogViewerBlend, self).__init__(*args, **kwargs)


class CatalogViewerPlugin(GUIPlugin):
    name = 'Catalog Viewer'
    def __init__(self):
        self.layout = QHBoxLayout()
        self.parent_widget = QWidget()
        self.field_label = QLabel('Select image:')
        self.field_combo_box = QComboBox()
        self.field_combo_box.setFixedWidth(300)
        self.layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        self.layout.addWidget(self.field_label)
        self.layout.addWidget(self.field_combo_box)
        self.parent_widget.setLayout(self.layout)
        self.field_combo_box.currentTextChanged.connect(self.field_changed)
        self.catalog_viewer = CatalogViewerBlend()
        self.stages = {'Viewer': GUILayout(top=self.parent_widget, 
                       center=self.catalog_viewer), }
        super(CatalogViewerPlugin, self).__init__()

    def field_changed(self, new_device):
        self.catalog_viewer.fieldChanged(new_device)

    def appendCatalog(self, run_catalog, **kwargs):
        self.catalog_viewer.setCatalog(run_catalog, 'primary', None)
        all_fields = run_catalog.primary.metadata['descriptors'][0]['data_keys']
        image_fields = []
        for field, field_descriptor in all_fields.items():
            field_shape = len(field_descriptor['shape'])
            if field_shape > 1 and field_shape < 5:
                image_fields.append(field)
        self.field_combo_box.clear()
        self.field_combo_box.addItems(image_fields)

    def appendHeader(self):
        ...
