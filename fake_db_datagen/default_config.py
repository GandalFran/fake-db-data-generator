#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


def serve_default_config():

    obj = {
        "schema": None,
        "data_types": {
            "base_types": {
                "datetime": {
                    "value": {
                        "start": "2020-01-01T10:00:00",
                        "end": "2023-01-01T10:00:00"
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "float": {
                    "value": {
                        "start": 0.0,
                        "end": 10.0
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "int": {
                    "value": {
                        "start": 0,
                        "end": 10
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "boolean": {
                    "value": {
                        "start": 0,
                        "end": 10
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                }
            },
            "collections": {
                "name": {
                    "pattern": "((.*)?name(.*)?)|((.*)?nombre(.*)?)",
                    "values": [
                        "Liam",
                        "Olivia",
                        "Noah",
                        "Emma",
                        "Oliver",
                        "Charlotte",
                        "Elijah",
                        "Amelia",
                        "James",
                        "Ava",
                        "William",
                        "Sophia",
                        "Benjamin",
                        "Isabella",
                        "Lucas",
                        "Mia",
                        "Henry",
                        "Evelyn",
                        "Theodore",
                        "Harper"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "surname": {
                    "pattern": "((.*)?apellido(.*)?)|((.*)?surname(.*)?)",
                    "values": [
                        "Smith",
                        "Johnson",
                        "Williams",
                        "Brown",
                        "Jones",
                        "Garcia",
                        "Miller",
                        "Davis",
                        "Rodriguez",
                        "Martinez",
                        "Hernandez",
                        "Lopez",
                        "Gonzalez",
                        "Wilson",
                        "Anderson",
                        "Thomas",
                        "Taylor",
                        "Moore",
                        "Jackson",
                        "Martin"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "addres": {
                    "pattern": "((.*)?addres(.*)?)|((.*)?direction(.*)?)|((.*)?location(.*)?)|((.*)?ubication(.*)?)|((.*)?dirección(.*)?)|((.*)?direccion(.*)?)|((.*)?localización(.*)?)|((.*)?ubicación(.*)?)|((.*)?localizacion(.*)?)|((.*)?ubicacion(.*)?)",
                    "values": [
                        "Address 1",
                        "Address 2",
                        "Address 3"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "sex": {
                    "pattern": "((.*)?sex(.*)?)|((.*)?gender(.*)?)|((.*)?género(.*)?)",
                    "values": [
                        "male",
                        "female",
                        "other"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "text": {
                    "pattern": "((.*)?text(.*)?)",
                    "values": [
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque maximus justo et est bibendum porttitor. Donec ultricies odio a sem aliquet consectetur. In facilisis mollis nisi. Quisque eu neque vitae enim dignissim lobortis at eu enim. Suspendisse tristique risus sit amet nisi consectetur gravida. Curabitur interdum libero lorem, vel consequat tellus sagittis sit amet. Proin nec ullamcorper risus. Nonea efficitur ullamcorper ipsum, in feugiat risus fringilla at. Proin tortor neque, mattis ut diam in, egestas fermentum mauris. Noneam sapien ante, pulvinar sit amet nisi vel, imperdiet sagittis ligula. Vivamus nec enim varius est posuere convallis sit amet nec felis. Curabitur imperdiet tincidunt tempor. Pellentesque hendrerit malesuada vulputate. Nonea vel dolor venenatis lorem porttitor euismod nec ut dolor.",
                        "Suspendisse vel maximus dui. Morbi ultricies dolor nec arcu maximus, in finibus nibh imperdiet. Cras libero diam, rutrum sit amet ante ac, facilisis finibus diam. Etiam ut lacus dui. Nam aliquam gravida turpis, ac consectetur nibh lacinia at. Vestibulum sollicitudin justo non risus maximus fringilla. Sed fringilla, risus vitae blandit tristique, felis libero tincidunt orci, in ultricies metus odio id nunc. In hac habitasse platea dictumst. In hac habitasse platea dictumst. Morbi lectus dui, laoreet et venenatis vitae, ullamcorper a massa. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque in elit viverra, convallis ipsum eu, suscipit nisi. Suspendisse id augue vel odio interdum vehicula elementum ac justo. Etiam eros tortor, tincidunt eu egestas eget, dictum vitae lacus. Nam est justo, lacinia maximus luctus eget, consequat sed justo. Suspendisse sagittis quis lacus vel vestibulum.",
                        "Etiam maximus vitae sapien sed elementum. Praesent felis metus, molestie nec posuere ultricies, maximus quis arcu. Pellentesque in lectus at urna aliquam maximus non in mi. Proin auctor, ex ut gravida faucibus, sapien mauris lacinia lorem, sed aliquam nisl est eu lectus. Aliquam non condimentum mi. Morbi vel magna sem. Nunc tincidunt molestie urna, sed pharetra justo sollicitudin vitae. Integer iaculis vehicula tortor, feugiat ornare enim dictum non.",
                        "Nam malesuada Nonea sit amet dui pretium fringilla quis vulputate ligula. Etiam porttitor massa sem, eu feugiat augue scelerisque in. Nonea fringilla ac quam sit amet hendrerit. Praesent nec massa convallis, venenatis turpis ac, blandit orci. Aenean a lorem sagittis, suscipit erat scelerisque, rutrum urna. Praesent et Nonea in mauris rutrum dignissim a sed lacus. Etiam luctus turpis ac leo vestibulum consectetur. Integer sed justo sit amet libero porttitor blandit ac in lacus. Donec id Nonea non dolor faucibus rutrum. Curabitur luctus pharetra ligula, sed vulputate ex luctus eget. Sed tristique convallis enim, nec ullamcorper dui vehicula eget. Donec ex turpis, scelerisque eu convallis efficitur, sagittis vel nisi. Praesent neque dolor, eleifend non porta a, varius vel massa.",
                        "Sed ligula velit, dictum id nibh vitae, cursus hendrerit massa. Proin lobortis erat orci, eu molestie urna mollis at. Pellentesque at sagittis velit, vel pellentesque lectus. Nam aliquam rutrum quam, quis molestie nisl iaculis quis. Vestibulum id pharetra risus, ac auctor leo. Noneam dignissim a neque at sagittis. Aenean suscipit ante in erat semper fermentum. Pellentesque vulputate sollicitudin sodales. Sed consequat porta felis ut rhoncus."
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                }
            },
            "generables": {
                "id": {
                    "pattern": "((.*)?id(.*)?)",
                    "samples": 10,
                    "generator": "[0-9]{1-10}"
                },
                "uuid": {
                    "pattern": "((.*)?uuid(.*)?)|((.*)?uid(.*)?)",
                    "samples": 10,
                    "generator": "[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
                },
                "phone": {
                    "pattern": "((.*)?phone(.*)?)|((.*)?movil(.*)?)|((.*)?móvil(.*)?)|((.*)?telefono(.*)?)|((.*)?teléfono(.*)?)",
                    "samples": 10,
                    "generator": "[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}"
                },
                "email": {
                    "pattern": "((.*)?email(.*)?)|((.*)?mail(.*)?)|((.*)?correo(.*)?)",
                    "samples": 10,
                    "generator": "[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}."
                },
                "ip": {
                    "pattern": "(.*)?ip(.*)?",
                    "samples": 10,
                    "generator": "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                },
                "dni": {
                    "pattern": "(.*)?dni(.*)?",
                    "samples": 10,
                    "generator": "[0-9]{7}[A-Z]{1}"
                },
                "varchar": {
                    "pattern": "varchar",
                    "samples": 10,
                    "generator": "[a-zA-Z]{1-255}"
                },
                "char": {
                    "pattern": "char",
                    "samples": 10,
                    "generator": "[a-zA-Z]{1}"
                }
            }
        }
    }

    return obj
