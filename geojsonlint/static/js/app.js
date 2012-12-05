var map;
$(document).ready(function() {
    map = new L.Map('map-container', {
        center: new L.LatLng(37.92686760148135, -96.767578125),
        zoom: 4,
        layers: [
            new L.TileLayer('http://{s}.tiles.mapbox.com/v3/jcsanford.map-xu5k4lii/{z}/{x}/{y}.png', {
                maxZoom: 16,
                subdomains: ['a', 'b', 'c', 'd'],
                attribution: 'Tiles Courtesy of <a href="http://www.mapbox.com/" target="_blank">MapBox</a>. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
            })
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
                layer.bindPopup(popupString);
            }
        }
    });

    map.addLayer(geojsonLayer);

    $('#submit').on('click', function() {
        if ($('#geojson-input').val().length < 1) {
            return;
        }
        try {
            var testJson = $('#geojson-input').val();
        } catch (e) {
            $('#modal-message-body').html(e.toString());
            $('#modal-message-header').html('Invalid JSON');
            $('#modal-message').modal('show');
            return;
        }
        validateGeoJSON(testJson, function(data) {
            if (data.status === 'ok') {
                if ($('#clear-current').attr('checked')) {
                    geojsonLayer.clearLayers();
                }
                geojsonLayer.addData(JSON.parse($('#geojson-input').val()));
                map.fitBounds(geojsonLayer.getBounds());
            } else if (data.status === 'error') {
                $('#modal-message-body').html(data.message);
                $('#modal-message-header').html('Invalid GeoJSON');
                $('#modal-message').modal('show');
            } else {
                $('#modal-message-body').html('An unknown error occured on the server. No one has been notified. You figure it out.');
                $('#modal-message-header').html('Invalid GeoJSON');
                $('#modal-message').modal('show');
            }
        });
    })

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

    showGeoJsonSample('Point');

    function validateGeoJSON(testJson, callback) {
        $.ajax({
            type: 'POST',
            url: '/validate',
            dataType: 'json',
            data: testJson,
            contentType: 'application/json',
            success: callback,
            error: function(jqXHR, textStatus, errorThrown) {
                
            }
        });
    }

    function showGeoJsonSample(geojsonType) {
        $('#geojson-input').val(JSON.stringify(window[geojsonType], null, 4));
    }
});
