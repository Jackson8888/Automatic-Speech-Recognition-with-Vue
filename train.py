import numpy as np
import tensorflow as tf
import automatic_speech_recognition as asr
# dataset = asr.dataset.Audio.from_csv('data/train.csv', batch_size=32)
# dev_dataset = asr.dataset.Audio.from_csv('dev.csv', batch_size=32)
dataset = asr.dataset.Audio.from_csv('data/TIMIT/timit_test.csv', batch_size=2)
dev_dataset = asr.dataset.Audio.from_csv(
    'data/TIMIT/timit_test.csv', batch_size=2)
alphabet = asr.text.Alphabet(lang='en')
features_extractor = asr.features.FilterBanks(
    features_num=160,
    winlen=0.02,
    winstep=0.01,
    winfunc=np.hanning
)
model = asr.model.get_deepspeech2(
    input_dim=160,
    output_dim=29,
    rnn_units=800,
    is_mixed_precision=False
)
# model.load_weights(
#     'automatic_speech_recognition/load/models/en-deepspeech2-weights-0.1.h5')
optimizer = tf.optimizers.Adam(
    lr=1e-4,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-8
)
decoder = asr.decoder.GreedyDecoder()
pipeline = asr.pipeline.CTCPipeline(
    alphabet, features_extractor, model, optimizer, decoder
)
pipeline.fit(dataset, dev_dataset, epochs=1)
pipeline.save('./checkpoint')

test_dataset = asr.dataset.Audio.from_csv(
    'data/TIMIT/timit_test.csv', batch_size=1)
wer, cer = asr.evaluate.calculate_error_rates(pipeline, test_dataset)
print(f'WER: {wer}   CER: {cer}')
