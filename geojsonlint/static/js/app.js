(function() {
var map;
$(document).ready(function() {
    var road_layer = new L.TileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
            maxZoom: 18,
            subdomains: ['1', '2', '3', '4'],
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
        }),
        satellite_layer = new L.TileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.png', {
            maxZoom: 18,
            subdomains: ['1', '2', '3', '4'],
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>.'
        }),
    map = new L.Map('map-container', {
        center: new L.LatLng(37.92686760148135, -96.767578125),
        zoom: 4,
        layers: [
            road_layer
        ]
    });

    var geojsonLayer = new L.GeoJSON(null, {
        onEachFeature: function (feature, layer) {
            if (feature.properties) {
                var popupString = '<div class="popup">';
                for (var k in feature.properties) {
                    var v = feature.properties[k];
                    popupString += k + ': ' + v + '<br />';
                }
                popupString += '</div>';
                layer.bindPopup(popupString, {
                    maxHeight: 200
                });
            }
        }
    });

    map.addLayer(geojsonLayer);

    L.control.layers({'Road': road_layer, 'Satellite': satellite_layer}, {'GeoJSON': geojsonLayer}).addTo(map);

    $('#submit').on('click', function() {
        if ($('#geojson-input').val().length < 1) {
            return;
        }
        var testJson = $('#geojson-input').val();

        var errors = geojsonhint.hint(testJson);

        if (errors.length > 0) {
          var message = errors.map(function(error) {
            return 'Line ' + error.line + ': ' + error.message;
          }).join('<br>')
          $('#modal-message-body').html(message);
          $('#modal-message-header').html('Invalid GeoJSON');
          $('#modal-message').modal('show');
        } else {
          if ($('#clear-current').attr('checked')) {
            geojsonLayer.clearLayers();
          }
          geojsonLayer.addData(JSON.parse($('#geojson-input').val()));
          map.fitBounds(geojsonLayer.getBounds());
        }
    });

    $('#clear').on('click', function() {
        $('#geojson-input').val('');
    });

    $('.modal-close').on('click', function(event) {
        event.preventDefault();
        $('#' + $(this).attr('id').split('-close')[0]).modal('hide');
    });

    $('a[data-toggle="tab"]').on('shown', function(event) {
        showGeoJsonSample($(event.target).attr('data-geojson-type'));
        $('#submit').trigger('click');
    });

    if (window.File && window.FileReader) {
        $('#geojson-input').on('dragenter', function (event) {
            showDroppable();
            event.preventDefault();
        });

        $('#geojson-input').on('dragleave', function (event) {
            hideDroppable();
            event.preventDefault();
        });

        $('#geojson-input').on('dragover', function (event) {
            event.preventDefault();
        });

        $('#geojson-input').on('drop', function (event) {
            event.preventDefault();

            hideDroppable();

            var dt = event.originalEvent.dataTransfer,
                files = dt.files,
                types = dt.types;

            if (files) {
                var file = files[0];

                if (file.name.indexOf('.json') !== -1 || file.name.indexOf('.geojson') !== -1) {
                    var reader = new FileReader();

                    reader.onload = function () {
                        $('#geojson-input').val(reader.result);
                    };

                    reader.readAsText(file);
                }
            }
        });
    }

    showGeoJsonSample('Point');

    function showGeoJsonSample(geojsonType) {
        $('#geojson-input').val(JSON.stringify(window[geojsonType], null, 4));
    }

    function showDroppable() {
        $('#geojson-input').addClass('drop-it');
    }

    function hideDroppable() {
        $('#geojson-input').removeClass('drop-it');
    }
});
}());
