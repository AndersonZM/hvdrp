# Output Specification for HVDRP

For the full problem specification and details, you should check the related papers of the problem linked in the [README.md](../README.md). Also, the input format for HVDRP should be located [here](input_format_hvdrp.md#top).

This system works with [json](https://www.json.org/json-en.html) files for output formating. The output files for HVDRP is formatted as `${INSTANCE_NAME}.hvdrp-out.json`.

The solution is divided into representation, evaluation and validation.
* The `representation` is the actual solution to the instance that specifies how the vehicle and the drones should move.
* The `evaluation` is a structure that details the objective function and some additional quantitative information of the solution.
* The `validation` is a structure that tells if the instance is valid and feasible. 
  * A *valid* solution respects the structural rules of the problem. E. g. no drones are left behind, all clients are visited exactly once, the vehicle doesn't repeat depots, and so on.
  * A *feasible* solution doesn't infringe the limits imposed by the problem. E. g. no drone flies beyond the maximum range, no drone carry more weight than they support, etc.
* The vertex labeling system and drone identification follows the same of the instance input. Check `input_format_hvdrp.md` for details. The drone is identified by its `id`. Each station is identified by `label`, where the depot has label *zero*.

```json
{
    "method": {
        "name": string,
        "parameters": { ... }
    },
    "instance": string,
    "time": fraction,
    "representation": {
        "vehiclePath": [ int, ..., int],
        "dronePath": [
            { "droneId": int, "start": int, "end": int, "clientOrder": [int, ..., int] },
            ...
            { "droneId": int, "start": int, "end": int, "clientOrder": [int, ..., int] }
        ]
    },
    "evaluation": {
        "totalCost": fraction,
        "vehicleCost": fraction,
        "droneCost": fraction,
        "stops": int,
        "dispatches": int        
    },
    "validation": {
        "valid": bool,
        "feasible": bool
    }
}
```

* The `method` object **optionally** tells which algorithm was used to devise the solution.
  * The `name` field inside `method` identifies the name of the application or algorithm used.
  * The `parameter` object describes the parameters used in the algorithm. For example, a method may list what seed or value for a calibratable parameter was used. Its format depends on the application used.
* The `instance` field tells the instance name that this solution refers to. This name follows the respective field specified at `input_format_hvdrp.md`. 
* The `time` field **optionally** tells how much time it took to devise the solution in seconds. 
* The `representation` object details the physical solution.
    * `vehiclePath` should be a permutation of stations using labels that dictates the vehicle vistation sequence. 
    * `dronePath` details the path that each drone take during the travel. Every drone flight must be in order based on the vehicle path. That is, for example, if the vehicle visits station *A* before *B*, every drone flight starting from *A* **must** be specified before any flight departing from *B*. Finally, for every drone path that departs from the same station, only the **last** one specified may end in a different stop alongside the vehicle tour.
        * `droneId` is the respective drone unique identifier
        * `start` is the departing stationg of this path. The drone flies as soon as the vehicle stops here.
        * `end` this is the station where the drone will be picked up after visiting all the clients.
        * `clientOrder` are the clients that this drone will fly to. They are visited in order.
* The `evaluation` field **optionally** details the objective function and some additional information.
    * `totalCost` is the objective cost itself.
    * `vehicleCost` is the total cost of the vehicle path.
    * `droneCost` is the total cost of all drone flights.
    * `stops` is the number of times that the vehicle stops in stations.
    * `dispatches` is the number of drone dispatches that the vehicle operates.
* The `valiadation` field **optionally** details if the solution is valid and feasible.
    * `valid` denotes that this solution respects the fundamental structure of the problem. E. g., drones may not be left behind, the vehicle has to visit each station just once, clients can only be visited once, all clients should be visited, etc.
    * `feasible` denotes if the solution respects the internal problem restrictions, i. e., the limit impose by the variables itself. E. g. the drone flight limit isn't supassed, and no drone carry more than their capacity.
