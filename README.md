# Bottom Up Synthesis
Repo for simple implementation of Bottom Up Synthesis for first class assignment. Implementation is based on non-ML BUSTLE algorithm presented in [BUSTLE: Bottom-up Program Synthesis Through Learning-guided Exploration](https://arxiv.org/pdf/2007.14381.pdf)

## Testing

### Full tests
To test the full implementation, please run:
```console
python src/bustle.py
```

### Arithmetic DSL
To test only the arithmetic DSL, please run:
```console
python src/bustle.py --mode 0
```

### String DSL
To test only the string manipulation DSL, please run:
```console
python src/bustle.py --mode 1
```
