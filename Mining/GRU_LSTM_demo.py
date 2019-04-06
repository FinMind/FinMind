

from FinMind.Data import Load
import numpy as np 
import pandas as pd
from keras.layers.core import Dense, Dropout
from keras.layers import LSTM , GRU
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
from keras.optimizers import Adam 

TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')

print('input data')
data = Load.FinData(
        dataset = 'TaiwanStockPrice',
        select = '2330.TW',
        date = '2010-01-01')

#colname = ['date', 'open', 'high', 'low', 'close', 'volume']
#data = data[colname]
print('select close price')
date = [ str(d) for d in data['date'] ]
stock_price = data['Close'].values.astype('float32')
stock_price = stock_price.reshape(len(stock_price), 1)

print(' 畫圖 ')
plt.plot(stock_price)
plt.show()

print(' 取 80% data 當作 training data, 20% data 當作 testing data 做模型驗證 ')
train_size = int(len(stock_price) * 0.8)
test_size = len(stock_price) - train_size
test_size = train_size + int(test_size/2)
valid_size = test_size

train = stock_price[:train_size,:]
test = stock_price[train_size:test_size,:]
valid = stock_price[valid_size:,:]

train_date = date[:train_size]
test_date = date[train_size:test_size]
valid_date = date[valid_size:]

print(' 歸一化 ')
scaler = MinMaxScaler(feature_range=(0, 1))
train = scaler.fit_transform(train)
test = scaler.transform(test)

print('切 data，拿前五天的股價，預測未來1天的股價，先做個 demo')
def process_data(data , n_features,future_days):
    dataX, dataY = [], []
    for i in range(len(data)-n_features-future_days):
        a = data[i:(i+n_features), 0]
        dataX.append(a)
        dataY.append(data[i + n_features-1+future_days, 0])
    return np.array(dataX), np.array(dataY)

# reshape into X=t and Y=t+5
n_features = 5
future_days = 1

trainX, trainY = process_data(train, n_features,future_days)
testX, testY = process_data(test, n_features,future_days)
print(trainX.shape , trainY.shape , testX.shape , testY.shape)

# lstm need input to have 3 dimensions
print('轉換成 LSTM 建模所需 data 的型態')
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

'''  set up DL model '''
print('設定參數')
filepath="stock_weights.hdf5"
from keras.callbacks import ReduceLROnPlateau , ModelCheckpoint
lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, epsilon=0.0001, patience=1, verbose=1)
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='max')

print('建立 DL 模型，使用 RNN 常見的 GRU and LSTM')
model = Sequential()
model.add(GRU(256 , input_shape = (1 , n_features) , return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(64 ,  activation = 'relu'))
model.add(Dense(1))
model.summary()

#model.load_weights('/home/linsam/job/stock_weight.h5')
model.compile(loss='mean_squared_error', optimizer=Adam(lr = 0.0005) , metrics = ['mean_squared_error'])
print('training')
history = model.fit(trainX, trainY, epochs=5 , batch_size = 128 , 
          callbacks = [checkpoint , lr_reduce] , validation_data = (testX,testY))
print(' save weight ')
model.save_weights('stock_weight.h5')


print('計算 error')
def model_score(model, X_train, y_train, X_test, y_test):
    trainScore = model.evaluate(X_train, y_train, verbose=0)
    print('Train Score: %.5f MSE (%.2f RMSE)' % (trainScore[0], math.sqrt(trainScore[0])))
    testScore = model.evaluate(X_test, y_test, verbose=0)
    print('Test Score: %.5f MSE (%.2f RMSE)' % (testScore[0], math.sqrt(testScore[0])))
    return trainScore[0], testScore[0]

tem = model_score(model, trainX, trainY , testX, testY)


pred = model.predict(testX)
pred = scaler.inverse_transform(pred)
print('\n Actual Stock Prices')
print( pred[:10] )

testY2 = testY.reshape(testY.shape[0] , 1)
testY2 = scaler.inverse_transform(testY2)
print('\n Predicted Stock Prices ')
print( testY2[:10] )

print('畫圖')
print("\nRed - Predicted Stock Prices  ,  Blue - Actual Stock Prices")
plt.rcParams["figure.figsize"] = (15,7)
plt.plot(testY2 , 'b')
plt.plot(pred , 'r')
plt.xlabel('Time')
plt.ylabel('Stock Prices')
plt.title('Red - Predicted Stock Prices  ,  Blue - Actual Stock Prices')
plt.grid(True)
plt.show()



























print('real predict')
tem = [ test_date.append(d) for d in valid_date ]
test2 = [ t[0] for t in test ]

valid2 = [ t[0] for t in scaler.transform(valid) ]
tem = [ test2.append(d) for d in valid2 ]

price = stock_price[train_size:,:]
price = [ p[0] for p in price ]

data2 = pd.DataFrame()
data2['price'] = price
data2['value'] = test2
data2['date'] = test_date

x = np.array([[[1,2,3,4,5]]])
pred = model.predict(x)
pred = scaler.inverse_transform(pred)









