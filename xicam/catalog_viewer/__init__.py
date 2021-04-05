from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView, StreamSelector, FieldSelector, CatalogImagePlotView


class CatalogViewerBlend(StreamSelector, FieldSelector, CatalogImagePlotView):
    def __init__(self, *args, **kwargs):
        # CatalogViewerBlend inherits methods from XArrayView and CatalogView
        # super allows us to access both methods when calling super() from Blend
        # field_filter None means all data will be selectable (not just default of image data)
        super(CatalogViewerBlend, self).__init__(*args, field_filter=None, **kwargs)


class CatalogViewerPlugin(GUIPlugin):
    name = "Catalog Viewer"

    def __init__(self):
        self.catalog_viewer = CatalogViewerBlend()
        self.stages = {
            "Viewer": GUILayout(center=self.catalog_viewer),
        }
        super(CatalogViewerPlugin, self).__init__()

    def appendCatalog(self, run_catalog, **kwargs):
        self.catalog_viewer.clear()
        try:
            msg.showMessage(f"Loading image for {run_catalog.name}")
            self.catalog_viewer.setCatalog(run_catalog)
        except Exception as e:
            msg.logError(e)
            msg.showMessage("Unable to display: ", str(e))
