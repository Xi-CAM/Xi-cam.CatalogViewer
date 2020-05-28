
from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView, StreamSelector, FieldSelector


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
        self.catalog_viewer.clear()
        try:
            msg.showMessage(f"Loading image for {run_catalog.name}")
            self.catalog_viewer.setCatalog(run_catalog)
        except Exception as e:
            msg.logError(e)
            msg.showMessage("Unable to display: ", str(e))
s