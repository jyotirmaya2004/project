import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint

def build_and_train_model(dataset_dir='dataset', epochs=10, batch_size=32):
    train_dir = os.path.join(dataset_dir, 'train')
    valid_dir = os.path.join(dataset_dir, 'valid')

    # 1. Load the PlantVillage dataset
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=(256, 256),
        batch_size=batch_size,
        label_mode='categorical'
    )
    class_names = train_ds.class_names

    val_ds = tf.keras.utils.image_dataset_from_directory(
        valid_dir,
        image_size=(256, 256),
        batch_size=batch_size,
        label_mode='categorical'
    )

    # 2. Preprocess inputs specifically for MobileNetV2 requirements (-1 to +1 range)
    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (preprocess_input(x), y), num_parallel_calls=tf.data.AUTOTUNE)

    train_ds = train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    # 3. Initialize MobileNetV2 (Freeze base model weights)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
    base_model.trainable = False

    # 4. Attach custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.4)(x)
    predictions = Dense(len(class_names), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    callbacks = [
        EarlyStopping(patience=3, restore_best_weights=True),
        TensorBoard(log_dir='tensorboard_logs/mobilenetv2_fit'),
        ModelCheckpoint('models/mobilenetv2_best.keras', save_best_only=True)
    ]

    print("Phase 1: Training the custom dense head layers...")
    model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)

    # 5. Fine-tuning the network
    print("Phase 2: Unfreezing base model layers and fine-tuning...")
    base_model.trainable = True

    # Keep the first 100 layers frozen, unfreeze the rest to retain low-level feature extraction
    for layer in base_model.layers[:100]:
        layer.trainable = False

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)

    # 6. Save the production-ready model
    os.makedirs('models', exist_ok=True)
    model.export('models/plant_leaf_disease_detector')
    with open('models/plant_leaf_disease_detector.classes.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(class_names) + '\n')
    with open('models/plant_leaf_disease_detector.preprocessing.txt', 'w', encoding='utf-8') as file:
        file.write('mobilenet_v2\n')
    print("Fine-tuned MobileNetV2 model exported successfully to 'models/plant_leaf_disease_detector'.")

if __name__ == '__main__':
    build_and_train_model()
