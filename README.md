# PSO dla robotów mobilnych

Implementacja algorytmu Particle Swarm Optimisation do doboru ścieżek przejazdu dla robota mobilnego po grafie. Implementacja wykorzystuje obliczenia macierzowe na karcie graficznej. 

Program jest wersją napisaną w języku Python i pokrywa się z napisaną wcześniej implementacją w języku C++.

## Wymagania

Program korzysta z implementacji pythona w wersji Python min. 3.7. wraz z Anaconda.
W programie wykorzystano biblioteki do zrównoleglania obliczeń na karcie graficznej:

```bash
conda install numba
```
Wskazówki do konfiguracji środowiska: https://numba.pydata.org/numba-doc/dev/user/installing.html

Wykorzystano także bibliotekę cupy
```bash
conda install cupy==91
```
## Uzycie
Wywowałanie programu wraz z ustawionymi parametrami można wykonać naprościej wykorzystując skrypt benchmark.py
```bash
python3 benchmark.py 
```

## Zastosowanie
Program został napisany przede wszystkim w celu przetestowania możliwości zrównoleglania obliczeń na kartach graficznych.


## License
[MIT](https://choosealicense.com/licenses/mit/)
