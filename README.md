# Hybrid Vehicle-Drone Routing Problem for Pick-up and Delivery Services

 This repository is an instance library for the hybrid vehicle-drone routing problem (HVDRP). The problem  was proposed by [Karak and Abdelghany (2019)](https://www.sciencedirect.com/science/article/abs/pii/S0968090X18312932). The main objective is to distribute an easily available collection of instances and their solutions to aid any research work related to this problem or any similar.

The best solution for each instance that the author of this repository knows is available as well. Please feel free to contact `azudio at id.uff.br` or make a pull request if you can support this library with additional instances or solutions followed by a description of the algorithm used or paper. Any submitted material should follow the same format documented at the [input_formar_hvdrp.md](input_format_hvdrp.md) and [output_format_hvdrp.md](output_format_hvdrp.md).   

* This repository is part of [Zudio et al (2021)](https://sbic.org.br/eventos/cbic_2021/cbic2021-107/) published at the proceedings of [CBIC 2021](https://sbic.org.br/eventos/cbic_2021/).

## Library Content

Every instance set is contained in its folder. They are comprised of easy to hard instances that follow different topologies. Check [input_formar_hvdrp.md](input_format_hvdrp.md) and [output_format_hvdrp.md](output_format_hvdrp.md) for details about the instance and solution format.

* `karak-benchmark` -- An intance set that follows the same topology used in [Karak and Abdelghany (2019)](https://www.sciencedirect.com/science/article/abs/pii/S0968090X18312932). Note that this *is not the actual instances used in the cited work*, they were generated using the tool available at the folder.
    * The solutions available for the subset `A-#` are the best solution.

## Algorithms

This section list any algorithm that may appear in a solution in this repository. An optional acronym in the `hvdrp-out.json` points to the method used.

* `BRKGAv0` -- A biased random key genetic algorithm described in [Zudio et al (2021)](https://sbic.org.br/eventos/cbic_2021/cbic2021-107/).
* `MIP-GRB` -- An implementation made by the owner of this repository using the [Gurobi](https://www.gurobi.com/) solver and the MIP detailed in [Karak and Abdelghany (2019)](https://www.sciencedirect.com/science/article/abs/pii/S0968090X18312932). 



