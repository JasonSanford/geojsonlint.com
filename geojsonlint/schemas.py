position = {
    "type": "array",
    "minItems": 2,
    "items": {
        "type": "number"
    }
}

point = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^Point$"
        },
        "coordinates": {
            "type": position
        }
    }
}

multipoint = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^MultiPoint$"
        },
        "coordinates": {
            "type": "array",
            "minItems": 2,
            "items": position
        }
    }
}

linestring = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^LineString$"
        },
        "coordinates": {
            "type": "array",
            "minItems": 2,
            "items": position
        }
    }
}

multilinestring = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^MultiLineString$"
        },
        "coordinates": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 2,
                "items": position
            }
        }
    }
}

polygon = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^Polygon$"
        },
        "coordinates": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 4,
                "items": position
            }
        }
    }
}

multipolygon = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^MultiPolygon$"
        },
        "coordinates": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 4,
                    "items": position
                }
            }
        }
    }
}

geometrycollection = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^GeometryCollection$"
        },
        "geometries": {
            "type": "array",
            "items": {
                "type": [
                    point,
                    multipoint,
                    linestring,
                    multilinestring,
                    polygon,
                    multipolygon
                ]
            }
        }
    }
}

feature = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^Feature$"
        },
        "properties": {
            "type": [
                "object",
                None
            ]
        },
        "geometry": {
            "type": [
                point,
                multipoint,
                linestring,
                multilinestring,
                polygon,
                multipolygon,
                geometrycollection,
                None
            ]
        }
    }
}

featurecollection = {
    "type": "object",
    "properties": {
        "type": {
            "pattern": "^FeatureCollection$"
        },
        "features": {
            "type": "array",
            "items": feature
        }
    }
}