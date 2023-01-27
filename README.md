# Fake DB data generation

Fake data generation tool with DBML.

## Usage
1. Install package with `python -m pip install . --upgrade`.
2. Prepare the configuration and DBML files.
3. Generate the components with `fakedatagen -d data.dbml -c config.json -o output.sql -f sql`.

## Configuration file

Example of configuration file

```json
{
    "schema":
    {
        "exampleTable":
        {
            "exampleField":
            {
                "type": "date",
                "value":
                {
                    "start": "2020-01-01T10:00:00.000Z",
                    "end": "2023-01-01T10:00:00.000Z",
                    "range": null
                },
                "distribution":
                {
                    "type": "normal"
                }
            }
        }
    },
    "data_types":
    {
        "collections": null,
        "generators": null
    }
}
```

Default configuration file

```json
{
    "schema": null,
    "data_types":
    {
        "base_types":
        {
            "date":
            {
                "value":
                {
                    "start": "2020-01-01T10:00:00.000Z",
                    "end": "2023-01-01T10:00:00.000Z",
                    "range": null
                },
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "time":
            {
                "value":
                {
                    "start": "00:00:00.000Z",
                    "end": "23:59:59.999Z",
                    "range": null
                },
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "float":
            {
                "value":
                {
                    "start": 0.0,
                    "end": 10.0,
                    "range": null
                },
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "int":
            {
                "value":
                {
                    "start": 0,
                    "end": 10,
                    "range": null
                },
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            }
        },
        "collections":
        {
            "name":
            {
                "pattern": "(name.*)|(nombre.*)",
                "values":
                [
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
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "surname":
            {
                "pattern": "(surmane.*)|(surname.*)",
                "values":
                [
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
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "address":
            {
                "pattern": "(*.address.*)|(*.dirección.*)|(*.direccion.*)",
                "values":
                [
                    "Address 1",
                    "Address 2",
                    "Address 3"
                ],
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "sex":
            {
                "pattern": "(*.sex.*)|(*.gender.*)|(*.género.*)",
                "values":
                [
                    "male",
                    "female",
                    "other"
                ],
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            },
            "text":
            {
                "pattern": "(*.text.*)",
                "value":
                [
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque maximus justo et est bibendum porttitor. Donec ultricies odio a sem aliquet consectetur. In facilisis mollis nisi. Quisque eu neque vitae enim dignissim lobortis at eu enim. Suspendisse tristique risus sit amet nisi consectetur gravida. Curabitur interdum libero lorem, vel consequat tellus sagittis sit amet. Proin nec ullamcorper risus. Nulla efficitur ullamcorper ipsum, in feugiat risus fringilla at. Proin tortor neque, mattis ut diam in, egestas fermentum mauris. Nullam sapien ante, pulvinar sit amet nisi vel, imperdiet sagittis ligula. Vivamus nec enim varius est posuere convallis sit amet nec felis. Curabitur imperdiet tincidunt tempor. Pellentesque hendrerit malesuada vulputate. Nulla vel dolor venenatis lorem porttitor euismod nec ut dolor.",
                    "Suspendisse vel maximus dui. Morbi ultricies dolor nec arcu maximus, in finibus nibh imperdiet. Cras libero diam, rutrum sit amet ante ac, facilisis finibus diam. Etiam ut lacus dui. Nam aliquam gravida turpis, ac consectetur nibh lacinia at. Vestibulum sollicitudin justo non risus maximus fringilla. Sed fringilla, risus vitae blandit tristique, felis libero tincidunt orci, in ultricies metus odio id nunc. In hac habitasse platea dictumst. In hac habitasse platea dictumst. Morbi lectus dui, laoreet et venenatis vitae, ullamcorper a massa. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque in elit viverra, convallis ipsum eu, suscipit nisi. Suspendisse id augue vel odio interdum vehicula elementum ac justo. Etiam eros tortor, tincidunt eu egestas eget, dictum vitae lacus. Nam est justo, lacinia maximus luctus eget, consequat sed justo. Suspendisse sagittis quis lacus vel vestibulum.",
                    "Etiam maximus vitae sapien sed elementum. Praesent felis metus, molestie nec posuere ultricies, maximus quis arcu. Pellentesque in lectus at urna aliquam maximus non in mi. Proin auctor, ex ut gravida faucibus, sapien mauris lacinia lorem, sed aliquam nisl est eu lectus. Aliquam non condimentum mi. Morbi vel magna sem. Nunc tincidunt molestie urna, sed pharetra justo sollicitudin vitae. Integer iaculis vehicula tortor, feugiat ornare enim dictum non.",
                    "Nam malesuada nulla sit amet dui pretium fringilla quis vulputate ligula. Etiam porttitor massa sem, eu feugiat augue scelerisque in. Nulla fringilla ac quam sit amet hendrerit. Praesent nec massa convallis, venenatis turpis ac, blandit orci. Aenean a lorem sagittis, suscipit erat scelerisque, rutrum urna. Praesent et nulla in mauris rutrum dignissim a sed lacus. Etiam luctus turpis ac leo vestibulum consectetur. Integer sed justo sit amet libero porttitor blandit ac in lacus. Donec id nulla non dolor faucibus rutrum. Curabitur luctus pharetra ligula, sed vulputate ex luctus eget. Sed tristique convallis enim, nec ullamcorper dui vehicula eget. Donec ex turpis, scelerisque eu convallis efficitur, sagittis vel nisi. Praesent neque dolor, eleifend non porta a, varius vel massa.",
                    "Sed ligula velit, dictum id nibh vitae, cursus hendrerit massa. Proin lobortis erat orci, eu molestie urna mollis at. Pellentesque at sagittis velit, vel pellentesque lectus. Nam aliquam rutrum quam, quis molestie nisl iaculis quis. Vestibulum id pharetra risus, ac auctor leo. Nullam dignissim a neque at sagittis. Aenean suscipit ante in erat semper fermentum. Pellentesque vulputate sollicitudin sodales. Sed consequat porta felis ut rhoncus."
                ],
                "distribution":
                {
                    "type": "normal",
                    "config": null
                }
            }
        },
        "generables":
        {

            "id":
            {
                "pattern": "(.*id.*)",
                "generator": "[0-9]{1-10}"
            },
            "uuid":
            {
                "pattern": "(.*uuid.*)|(.*uid.*)",
                "generator": "[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
            },
            "phone":
            {
                "pattern": "(.*phone.*)|(.*movil.*)|(.*móvil.*)|(.*telefono.*)|(.*teléfono.*)",
                "generator": "[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}"
            },
            "email":
            {
                "pattern": "(*.email.*)|(*.mail.*)|(*.correo.*)",
                "generator": "[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}."
            },
            "ip":
            {
                "pattern": ".*ip.*",
                "generator": "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
            },
            "dni":
            {
                "pattern": "*dni*",
                "generator": "[0-9]{7}[A-Z]{1}"
            },
            "varchar":
            {
                "pattern": "varchar",
                "generator": "[a-zA-Z]{1-255}"
            },
            "char":
            {
                "pattern": "char",
                "generator": "[a-zA-Z]{1}"
            }
        }
    }
}
```
