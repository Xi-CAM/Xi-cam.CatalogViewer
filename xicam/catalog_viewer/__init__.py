from qtpy.QtWidgets import QLabel, QComboBox, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from xicam.core import msg
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.imageviewmixins import XArrayView, CatalogView, StreamSelector, FieldSelector
import logging
from xicam.core import msg

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
            stream_names = get_all_streams(run_catalog)

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


### small helper functions
def get_stream_data_keys(run_catalog, stream):
    return run_catalog[stream].metadata["descriptors"][0]["data_keys"]


def get_all_streams(run_catalog):
    return list(run_catalog)


def get_all_image_fields(run_catalog):
    # image_fields = []
    all_streams_image_fields = {}
    for stream in get_all_streams(run_catalog):
        stream_fields = get_stream_data_keys(run_catalog, stream)
        field_names = stream_fields.keys()
        for field_name in field_names:
            field_shape = len(stream_fields[field_name]["shape"])
            if field_shape > 1 and field_shape < 5:
                # if field contains at least 1 entry that is at least one-dimensional (shape=2)
                # or 2-dimensional (shape=3) or up to 3-dimensional (shape=4)
                # then add field e.g. 'fccd_image'
                if stream in all_streams_image_fields.keys():  # add values to stream dict key
                    all_streams_image_fields[stream].append(field_name)
                else:  # if stream does not already exist in dict -> create new entry
                    all_streams_image_fields[stream] = [field_name]
            # TODO how to treat non image data fields in streams
            # else:
    return all_streams_image_fields


# Problem: primary image field does not show up anymore...
# Problem: primary image field does not show up anymore...
