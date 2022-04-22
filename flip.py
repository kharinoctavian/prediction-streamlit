import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier

def trained_model():
  datatrain=pd.read_csv(r'data train numerik no box 20 k5 91.csv')

  datatrain["DERMAGA"]=datatrain["DERMAGA"].astype('category')
  datatrain["JENIS_KAPAL"]=datatrain["JENIS_KAPAL"].astype('category')
  datatrain["DELAY"]=datatrain["DELAY"].astype('category')
  datatrain["PALKA"]=datatrain["PALKA"].astype('int')
  datatrain["BD"]=datatrain["BD"].astype('int')
  datatrain["SHIFTING"]=datatrain["SHIFTING"].astype('int')
  datatrain["WAG"]=datatrain["WAG"].astype('int')
  datatrain["BAD_WEATHER"]=datatrain["BAD_WEATHER"].astype('int')
  datatrain["JUMLAH_CC"]=datatrain["JUMLAH_CC"].astype('int')
  datatrain["DISCHARGE"]=datatrain["DISCHARGE"].astype('int')
  datatrain["LOADING"]=datatrain["LOADING"].astype('int')
  
  arr = datatrain.values
  X_train = arr[:, :-1]
  Y_train = arr[:, -1]

  datatest=pd.read_csv(r'data test numerik no box 20 k5 91.csv')

#tambahin ubah data integer
  datatest["DERMAGA"]=datatest["DERMAGA"].astype('category')
  datatest["JENIS_KAPAL"]=datatest["JENIS_KAPAL"].astype('category')
  datatest["DELAY"]=datatest["DELAY"].astype('category')
  datatest["PALKA"]=datatest["PALKA"].astype('int')
  datatest["BD"]=datatest["BD"].astype('int')
  datatest["SHIFTING"]=datatest["SHIFTING"].astype('int')
  datatest["WAG"]=datatest["WAG"].astype('int')
  datatest["BAD_WEATHER"]=datatest["BAD_WEATHER"].astype('int')
  datatest["JUMLAH_CC"]=datatest["JUMLAH_CC"].astype('int')
  datatest["DISCHARGE"]=datatest["DISCHARGE"].astype('int')
  datatest["LOADING"]=datatest["LOADING"].astype('int')
  
  arr = datatest.values
  X_test = arr[:, :-1]
  Y_test = arr[:, -1]

  knn=KNeighborsClassifier(n_neighbors=5)
  knn.fit(X_train,Y_train)
  Y_PredKNN=knn.predict(X_test)
  #Saving the Model
  pickle_out = open("knn.pkl", "wb") 
  pickle.dump(knn, pickle_out) 
  pickle_out.close()
  
  

def prediction(DERMAGA, JENIS_KAPAL, PALKA, JUMLAH_CC, DISCHARGE, LOADING, BD, SHIFTING_YARD, WAG, BAD_WEATHER):
  pickle_in = open('knn.pkl', 'rb')
  classifier = pickle.load(pickle_in)
  
  prediction = classifier.predict([[DERMAGA, JENIS_KAPAL, PALKA, JUMLAH_CC, DISCHARGE, LOADING, BD, SHIFTING_YARD, WAG, BAD_WEATHER]])
  probas = classifier.predict_proba([[DERMAGA, JENIS_KAPAL, PALKA, JUMLAH_CC, DISCHARGE, LOADING, BD, SHIFTING_YARD, WAG, BAD_WEATHER]])
  st.write("Peluang Prediksi pada Masing-Masing Kategori Delay")
  probability = "{:.2f}".format(float(probas[:, 0]))
  st.write("TIDAK DELAY : ", probability)
  
  probability = "{:.2f}".format(float(probas[:, 1]))
  st.write("DELAY KURANG DARI 4 JAM : ", probability)
  
  probability = "{:.2f}".format(float(probas[:, 2]))
  st.write("DELAY LEBIH DARI 4 JAM : ", probability)
  
  #tabel prediksi
  #st.write(prediction)
  if prediction == 0:
    pred = 'KAPAL TIDAK MENGALAMI DELAY KEBERANGKATAN'
  elif prediction == 1:
    pred = 'KAPAL MENGALAMI DELAY KURANG DARI 4 JAM'
  else:
    pred = 'KAPAL MENGALAMI DELAY LEBIH DARI 4 JAM'
  return pred

def main():
  st.header('Prediksi Delay Keberangkatan Kapal')
  JENIS_KAPAL = st.selectbox("Jenis Kapal:", ("Feeder", "Direct"))
  DERMAGA = st.selectbox("Dermaga Sandar:", ("1", "2", "3", "4"))
  PALKA = st.number_input("Jumlah Palka (Unit):", min_value=0, max_value=10000, value=0, step=1)
  BD = st.number_input("Lama Waktu Breakdown (Menit):", min_value=0, max_value=10000, value=0, step=1)
  SHIFTING_YARD = st.number_input("Jumlah Shifting Yard (Box):", min_value=0, max_value=10000, value=0, step=1)
  WAG = st.number_input("Lama Waktu WAG (Menit):", min_value=0, max_value=10000, value=0, step=1)
  BAD_WEATHER = st.number_input("Lama Waktu Bad Weather (Menit):", min_value=0, max_value=10000, value=0, step=1)
  JUMLAH_CC = st.number_input("Jumlah CC (Unit):", min_value=0, max_value=10000, value=0, step=1)
  DISCHARGE = st.number_input("Jumlah Petikemas yang Dibongkar (Box):", min_value=0, max_value=10000, value=0, step=1)
  LOADING = st.number_input("Jumlah Petikemas yang Dimuat (Box):", min_value=0, max_value=10000, value=0, step=1    )
  submit = st.button('Predict')
  if submit:
    if JENIS_KAPAL == "Direct":
      JENIS_KAPAL = 1
    else:
      JENIS_KAPAL = 0
    if DERMAGA == "1":
      DERMAGA = 1
    elif DERMAGA == "2":
      DERMAGA = 2
    elif DERMAGA == "3":
      DERMAGA = 3
    else:
      DERMAGA = 4
    trained_model()
    st.text("")
    result = prediction(JENIS_KAPAL, DERMAGA, PALKA, BD, SHIFTING_YARD, WAG, BAD_WEATHER, JUMLAH_CC, DISCHARGE, LOADING)
    st.success(format(result))
      
if __name__ == '__main__':
  main()
