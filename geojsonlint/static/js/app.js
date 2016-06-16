(function() {
  var map;

  $(document).ready(function() {
    L.mapbox.accessToken = 'pk.eyJ1IjoiamNzYW5mb3JkIiwiYSI6InRJMHZPZFUifQ.F4DMGoNgU3r2AWLY0Eni-w';
    map = L.mapbox.map('map-container', 'mapbox.streets')
    map.setView([37.92686, -96.76757], 4);

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
