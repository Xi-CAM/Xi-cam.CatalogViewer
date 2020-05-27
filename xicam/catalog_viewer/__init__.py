from qtpy.QtWidgets import QLabel, QComboBox, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView, StreamSelector, FieldSelector
import logging
from xicam.core import msg
from xicam.core.data.bluesky_utils import get_all_image_fields
# log = logging.getLogger('catalog_viewer')


class CatalogViewerBlend(StreamSelector, FieldSelector, XArrayView, CatalogView):
    def __init__(self, *args, **kwargs):
        # CatalogViewerBlend inherits methods from XArrayView and CatalogView
        # super allows us to access both methods when calling super() from Blend
        super(CatalogViewerBlend, self).__init__(*args, **kwargs)


class CatalogViewerPlugin(GUIPlugin):
    name = "Catalog Viewer"

    def __init__(self):
        self.catalog_viewer = CatalogViewerBlend()
        self.stages = {
            "Viewer": GUILayout(center=self.catalog_viewer),
        }
        super(CatalogViewerPlugin, self).__init__()

    def appendCatalog(self, run_catalog, **kwargs):
        try:
            self.stream_fields = get_all_image_fields(run_catalog)
            stream_names = list(run_catalog)

            msg.showMessage(f"Loading primary image for {run_catalog.name}")
            # try and startup with primary catalog and whatever fields it has
            if "primary" in self.stream_fields:
                default_stream_name = "primary" if "primary" in stream_names else stream_names[0]
            else:
                default_stream_name = list(self.stream_fields.keys())[0]
            self.catalog_viewer.setCatalog(run_catalog, default_stream_name, None)
        except Exception as e:
            msg.logError(e)
            msg.showMessage("Unable to display: ", str(e))

# Problem: primary image field does not show up anymore...
# Problem: primary image field does not show up anymore...
