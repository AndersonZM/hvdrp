# Input Specification for HVDRP

For the full problem specification and details, you should check the related papers of the problem linked in the [README.md](README.md). The output format for HVDRP used in this project is documented [here](output_format_hvdrp.md).

This system works with [json](https://www.json.org/json-en.html) files for input formating. The instance files for HVDRP uses the format `${INSTANCE_NAME}.hvdrp.json`. It is recommended that each instance have an unique name inside the project for solution mapping purposes.

* Originally, instances are described by a directed graph. But several cases can be simplified to work with an undirected graph, where the cost of travelling with each drone or the vehicle is given by a multiplicative factor. Thererfore, this system has two type of instances:
  * **Symmetric instances** are described through coordinates in a 2D plane using Euclidean distance. The distance of any arc of the form $A(i, j)$ equals to the distance of $A(j, i)$, $\forall i \neq j$. It is assumed that every edge exists and can be travelled. The vehicle and each drone travel cost is detailed by a respective multiplicative factor of the edge distance.
  * **Asymmetric instances** are described by a detailed description of each arc. The edge distance, cost of travel for the vehicle, and cost of flying for each drone should be discriminated individually. Nothing is assumed. Arcs that can't be travelled should be denoted with a value of minus one.

## Symmetric instance structure

A symmetric instance has the following JSON structure:

```json

{
    "name": string,
    "symmetric": {
        "droneSpecification": [
            { "id": int, "range": fraction, "weight": fraction, "cost": fraction },
            ...
            { "id": int, "range": fraction, "weight": fraction, "cost": fraction }
        ],
        "vehicleCost": fraction,
        "depotCoordinates": { "x": fraction, "y": fraction },
        "stationCoordinates": [
            { "label": int, "x": fraction, "y": fraction },
            ...
            { "label": int, "x": fraction, "y": fraction }
        ],
        "clientCoordinates": [
            { "label": int, "x": fraction, "y": fraction, "delivery": fraction, "pickup": fraction },
            ...
            { "label": int, "x": fraction, "y": fraction, "delivery": fraction, "pickup": fraction }
        ]
    }
}

```
* `name` state the instance name. The file should be named after this field.  It is recommended to be unique across the project.
* The `symmetric` object details that the instance type is symmetric.
* The `droneSpecification` details how each drone is by its maximum `range` limit, maximum carry `weight` limit, and a multiplicative factor that is used to calculate its respective drone flying `cost`. Each drone has a unique identifier for solution mapping purposes. The first drone `id` should be zero and the last should be `id := #drones - 1`.
* The `vehicleCost` explicits a multiplicative factor that should be multiplied by each edge to obtain the respective vehicle cost of traveling.
* The `depotCoordinates` informs the coordinates of the starting depot.
* The `stationCoordinates` informs the coordinates of each station. The `label` should be its unique identifier for solution and graph mapping purposes: the first station should be labeled as `label := 1` and the last as `label := #stations`. **The zero value is reserved for the depot itself**.
* The `clientCoordinates` details all clients through coordinates and delivery & pickup information. The `label` works extacly as specified for stations: the first client should have `label := #stations+1` and the last `label := #clients + #stations` for solution and graph mapping purposes.

## Asymmetric instance sctructure

A asymmetric instance has the following JSON structure:

```json
{
    "name": string,
    "asymmetric": {
        "droneSpecification": [
            { "id": int, "range": fraction, "weight": fraction },
            ...
            { "id": int, "range": fraction, "weight": fraction }
        ],
        "clientSpecification": [
            { "label": int, "delivery": fraction, "pickup": fraction },
            ...
            { "label": int, "delivery": fraction, "pickup": fraction }
        ],
        "arcSpecification": {
            "numberStations": int,
            "arcs": [
                { "i": int, "j": int, "distance": fraction, "vehicleCost": fraction, "droneCost": [ fraction, ..., fraction ] },
                ...
                { "i": int, "j": int, "distance": fraction, "vehicleCost": fraction, "droneCost": [ fraction, ..., fraction ] }
            ]
        }
    }
}
```

* `name` states the instance name. The file should be named after this.  It is recommended to be unique across the project.
* The `asymmetric` object tells that the instance is asymmetric.
* The `droneSpecification` describe each drone by its maximum `range` limit, and maximum carry `weight`. Each drone has a unique identifier for solution mapping purposes. The first drone `id` should be zero and the last should be `id := #drones - 1`.
* The `clientSpecification` describes how each client is by `delivery` and `pickup` package weight. The `label` refers to the number of the vertex itself. The first client should be labeled as `#stations+1`, and the last should have `label := #clients + #stations`. 
* The `arcSpecification` details how each arc is. You should specify the number of stations with the field `numberStations` for labelling purposes. It is implicit that the label of the first station is *one* and the last is `#stations`. The `label := 0` refers to the depot itself.
    * An arc is structure given by the field `arc`, where `i` and `j` are the labels that denotes a link. The `distance` field is the link distance, `vehicleCost` the vehicle travel cost, and `droneCost` is an array with a real number for each drone in the instance that tells the respective flying cost of each sorted by id. Any negative `-1` value means that the arc cannot be trespassed by the vehicle or some drone. 

To summarize, the vertex labeling work as follows:

* The vertex `0` is the `depot`.
* Vertex labeled as `v := 1 to #stations` are stations.
* Each vertex from `v := (#stations + 1)` to `(#stations + #clients)` is a client.
* Drone `id` should be a value between `0` and `#drones - 1`.