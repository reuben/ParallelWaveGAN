# Parallel WaveGAN fork for Mozilla TTS
This is a fork of the [original](https://github.com/kan-bayashi/ParallelWaveGAN) implementation to sync with [Mozilla TTS](https://github.com/mozilla/TTS).

# Basic workflow
1. Create spectrograms using TTS based audio processing 
```python python bin/preprocess_tts.py```
2. Setup the config file wrt audio processing parameters used in your TTS model. Sample config can be found under ```parallel_wavegan/tts_config_v2.yaml```.
3. Train the model.
```python python parallel_wavegan/bin/train.py --config tts_config_v2.yaml --outdir /path/to/your/output/```

