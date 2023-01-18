import tensorflow_addons as tfa
from tensorflow import keras

from Create_Model import create_model


def train_model(train_ds, val_ds,
                model=create_model(), epochs=20,
                checkpoint_filepath="/tmp/checkpoint",
                optimizer=tfa.optimizers.AdaBelief(learning_rate=1e-3,
                                                   total_steps=10000,
                                                   warmup_proportion=0.1,
                                                   min_lr=2e-6,
                                                   rectify=True)):

    checkpoint_callback = keras.callbacks.ModelCheckpoint(checkpoint_filepath,
                                                          monitor="val_accuracy",
                                                          save_best_only=True,
                                                          save_weights_only=True)

    model.compile(optimizer=optimizer,
                  loss=keras.losses.BinaryFocalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # TODO: Find a solution to the problem of large transformer sequence.
    #       Which can lead to insufficient Graph Memory.

    try:
        # Fit the model on the batches generated by datagen.flow().
        history = model.fit(train_ds,
                            epochs=epochs,
                            validation_data=val_ds,
                            callbacks=[checkpoint_callback])
    except:
        history = None
        print("Do not have enough memory.")

    model.load_weights(checkpoint_filepath)

    return model, history
