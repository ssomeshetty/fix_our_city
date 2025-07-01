from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, Model

base = EfficientNetB0(include_top=False, weights='imagenet', pooling='avg')
base.trainable = False

inp = layers.Input(shape=(224, 224, 3))
x = base(inp, training=False)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
out = layers.Dense(2, activation='softmax')(x)

model = Model(inp, out)
model.compile(optimizer='adam', loss=focal_loss, metrics=['accuracy', 'AUC']) 
